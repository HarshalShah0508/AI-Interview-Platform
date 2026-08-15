import json
from google.genai import types

from app.core.config import GEMINI_MODEL

from app.services.api_key_manager import (
    api_key_manager,
)
from app.schemas.resume_analysis import (
    JDRequirement,
    SemanticVerification,
    SemanticVerificationBatch,
)


class SemanticVerifier:
    """
    Performs contextual verification only when the
    deterministic matcher cannot confidently classify
    a JD requirement.

    IMPORTANT:
    This service is not allowed to create resume evidence.

    All ambiguous requirements for one analysis are verified
    in a SINGLE Gemini call (see verify_batch) rather than one
    call per requirement, to keep the overall analysis within
    the project's Gemini call budget.

    Each requirement is given ONLY its own retrieved evidence
    (a small, ranked list of relevant resume lines chosen by
    RequirementMatcher._retrieve_relevant_evidence) instead of
    the entire resume — this keeps the prompt focused, keeps
    the request cheap, and makes it possible to validate that
    every "supporting_evidence" item Gemini cites actually came
    from the evidence it was given.
    """

    def verify_batch(
        self,
        requirements: list[JDRequirement],
        evidence_map: dict[str, list[str]],
    ) -> dict[str, SemanticVerification]:

        if not requirements:
            return {}

        requirement_blocks = []

        for index, requirement in enumerate(
            requirements,
            start=1,
        ):
            evidence_lines = evidence_map.get(
                requirement.name,
                [],
            )

            if evidence_lines:

                evidence_block = "\n".join(
                    f"{line_index}. {text}"
                    for line_index, text in enumerate(
                        evidence_lines,
                        start=1,
                    )
                )

            else:

                evidence_block = (
                    "(No potentially relevant resume "
                    "evidence was retrieved for this "
                    "requirement.)"
                )

            requirement_blocks.append(
                f"""
REQUIREMENT #{index}

requirement_name (echo this exactly):
{requirement.name}

Category:
{requirement.category}

Importance:
{requirement.importance}

JD Evidence:
{requirement.evidence}

Possible aliases:
{requirement.aliases}

Allowed resume evidence for THIS requirement:
{evidence_block}
"""
            )

        prompt = f"""
You are the Semantic Verification Engine
for HotSeat.

Your ONLY task is to determine, for EACH job-description
requirement listed below, whether the candidate's EXISTING
resume evidence satisfies that requirement.

You are verifying {len(requirements)} requirement(s) in
this single request. Return one verification object per
requirement, using the exact "requirement_name" value given
for each requirement so results can be matched back up.

Each requirement lists its OWN "Allowed resume evidence"
block. Use ONLY that requirement's own evidence block when
evaluating it. Do NOT borrow evidence from a different
requirement's block, and do NOT use any information about
the candidate that is not explicitly present in the
requirement's own evidence block.

JOB DESCRIPTION REQUIREMENTS
=============================

{"".join(requirement_blocks)}


STRICT RULES
============

1. You may ONLY use information present in the requirement's
own "Allowed resume evidence" block above.

2. NEVER invent experience.

3. NEVER assume that knowledge of one technology
means knowledge of another.

Examples:

Python does NOT imply Django.

Docker does NOT imply Kubernetes.

AWS does NOT imply Azure.

PostgreSQL does NOT imply MySQL.

React does NOT imply Next.js.

4. Do not infer a technology merely because it is
commonly used with another technology.

5. Do not infer years of experience unless explicitly
supported.

6. Do not infer leadership unless explicitly supported.

7. Do not infer production experience unless
explicitly supported.

8. Do not infer a specific cloud platform from
generic "cloud" experience.

9. Do not infer a specific database from generic
"database" experience.

10. A conceptually related statement can be considered
a PARTIAL match when it genuinely overlaps with the
requirement but does not prove the exact requirement.

Example:

JD:
"Distributed systems"

Resume:
"Built scalable backend services"

Possible result:
partial

NOT:
strong

11. A direct technology mention with meaningful usage
evidence can be strong.

Example:

JD:
"FastAPI"

Resume:
"Developed REST APIs using FastAPI"

Result:
strong

12. Generic statements without enough evidence should
remain ambiguous or missing.

13. Every "supporting_evidence" item you return MUST be an
exact or near-exact excerpt from that requirement's own
"Allowed resume evidence" block. Do not paraphrase, combine,
or invent evidence. If you cannot quote real evidence from
the block, do not claim support.

14. Do not rewrite or improve the resume.

15. Do not suggest adding anything.

16. If the evidence is insufficient, say so — use decision
"missing" rather than stretching a weak signal into
"partial" or "strong".

17. Confidence represents confidence in the decision,
NOT how impressive the candidate is.

18. unsupported_assumptions must explicitly identify
any assumption that would be required to classify
the candidate more strongly.

19. Evaluate each requirement independently using only its
own evidence block. Evidence that supports one requirement
must not be reused to justify a different, unrelated
requirement.

Return ONLY structured data matching the requested schema,
with exactly one verification per requirement listed above.
"""

        response = api_key_manager.generate_content(
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SemanticVerificationBatch,
            ),
            purpose="semantic_verification_batch",
        )

        raw = (
            response.text or ""
        ).strip()

        if not raw:
            raise ValueError(
                "Semantic verifier returned an empty response."
            )

        try:
            parsed = json.loads(raw)

            batch = SemanticVerificationBatch.model_validate(
                parsed
            )

        except Exception as exc:
            raise ValueError(
                "Semantic verifier returned invalid "
                "structured data."
            ) from exc

        results: dict[str, SemanticVerification] = {}

        for item in batch.verifications:
            results[item.requirement_name.strip().lower()] = item

        return results

import json
from google.genai import types

from app.core.config import (
    GEMINI_MODEL,
    GEMINI_SEMANTIC_VERIFICATION_BATCH_SIZE,
)

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
    a JD requirement, plus a second look at "missing"
    requirements that still have some loosely related
    retrieved evidence.

    IMPORTANT:
    This service is not allowed to create resume evidence.

    Requirements for one analysis are verified in chunked
    batched Gemini calls (see verify_batch), at most
    GEMINI_SEMANTIC_VERIFICATION_BATCH_SIZE requirements per
    call, rather than one call per requirement, to keep each
    call's structured response small and reliable while still
    keeping the overall analysis within a bounded call budget.
    If one chunk's call fails, only that chunk's requirements
    fall back to the conservative "missing" handling in
    RequirementMatcher._merge_verification — it does not fail
    the whole analysis.

    Each requirement is given its own retrieved evidence (a
    small, ranked list of relevant resume lines chosen by
    RequirementMatcher._retrieve_relevant_evidence) as a
    focused hint, PLUS the complete flattened resume evidence
    as a shared reference for the whole batch — retrieval can
    miss real evidence phrased in a way no search term
    anticipated, so the complete evidence lets Gemini still find
    and cite it. Every "supporting_evidence" item Gemini cites
    is still validated against what it was actually given
    (RequirementMatcher._merge_verification), so it can never
    cite text that doesn't genuinely exist in the resume.
    """

    def verify_batch(
        self,
        requirements: list[JDRequirement],
        evidence_map: dict[str, list[str]],
        adjacency_hints: dict[str, list[str]] | None = None,
        full_resume_evidence: list[str] | None = None,
    ) -> dict[str, SemanticVerification]:
        """
        Splits `requirements` into chunks of at most
        GEMINI_SEMANTIC_VERIFICATION_BATCH_SIZE and verifies
        each chunk via its own Gemini call, merging results.
        """

        if not requirements:
            return {}

        adjacency_hints = adjacency_hints or {}
        full_resume_evidence = full_resume_evidence or []

        chunk_size = GEMINI_SEMANTIC_VERIFICATION_BATCH_SIZE

        chunks = [
            requirements[start:start + chunk_size]
            for start in range(
                0,
                len(requirements),
                chunk_size,
            )
        ]

        results: dict[str, SemanticVerification] = {}

        for chunk_index, chunk in enumerate(
            chunks,
            start=1,
        ):

            try:

                chunk_results = self._verify_batch_chunk(
                    chunk,
                    evidence_map,
                    adjacency_hints,
                    full_resume_evidence,
                    chunk_index,
                    len(chunks),
                )

                results.update(chunk_results)

            except Exception:

                # Conservative degrade: this chunk's
                # requirements simply stay absent from
                # `results`. _merge_verification already
                # treats a missing verification as "no result
                # returned" -> falls back to
                # match_type="missing", score 0. One
                # malformed/failed chunk must not fail the
                # whole analysis.
                continue

        return results

    def _verify_batch_chunk(
        self,
        requirements: list[JDRequirement],
        evidence_map: dict[str, list[str]],
        adjacency_hints: dict[str, list[str]],
        full_resume_evidence: list[str],
        chunk_index: int,
        total_chunks: int,
    ) -> dict[str, SemanticVerification]:

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

            hinted_technologies = adjacency_hints.get(
                requirement.name,
                [],
            )

            if hinted_technologies:

                adjacency_line = (
                    "\nKnown related-but-NOT-equivalent tools, "
                    "technologies, or standards detected in "
                    "this candidate's resume: "
                    + ", ".join(hinted_technologies)
                    + "\n"
                )

            else:

                adjacency_line = ""

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
{adjacency_line}"""
            )

        if full_resume_evidence:

            full_resume_block = "\n".join(
                f"{line_index}. {text}"
                for line_index, text in enumerate(
                    full_resume_evidence,
                    start=1,
                )
            )

        else:

            full_resume_block = (
                "(No resume evidence was extracted for this "
                "candidate.)"
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
block — a focused, retrieval-ranked subset most likely to be
relevant to that specific requirement. Below that, a shared
"COMPLETE RESUME EVIDENCE" section lists every evidence line
extracted from this candidate's ENTIRE resume. The focused
block is a starting point, not a limit — if a requirement's
true supporting evidence exists elsewhere in the complete
resume evidence but was not included in its focused subset,
you may still cite it there, as long as it is a real, exact
excerpt from the complete resume evidence and is genuinely
relevant to that SPECIFIC requirement. Do NOT use any
information about the candidate that is not explicitly
present in either the requirement's own focused block or the
complete resume evidence section — nothing outside these two
sources.

JOB DESCRIPTION REQUIREMENTS
=============================

{"".join(requirement_blocks)}

COMPLETE RESUME EVIDENCE
=============================
(Shared reference for every requirement above.)

{full_resume_block}


STRICT RULES
============

1. You may ONLY use information present in the requirement's
own "Allowed resume evidence" block, or in the shared
"COMPLETE RESUME EVIDENCE" section — nothing else.

2. NEVER invent experience.

3. Knowledge of one tool, technology, or standard does NOT
automatically prove knowledge of a DIFFERENT, non-
interchangeable one in the same category, even when they are
commonly paired or compared.

3a. When the resume shows REAL, groundable evidence of a tool,
technology, or standard that is related-but-distinct from the
required one in the SAME category (e.g. a different cloud
platform, a different container orchestrator, a different
relational database, a different frontend framework, a
different CRM platform, a different accounting standard) — and
especially when a "Known related-but-NOT-equivalent tools,
technologies, or standards detected" hint is present for that
requirement — use decision "adjacent", NOT "partial" and NOT
"missing". "adjacent" means: real, grounded evidence exists,
but it is evidence of a DIFFERENT tool/technology/standard that
is transferable to, not proof of, the required one.

Worked example (technical):

JD:
"AWS experience required"

Resume evidence:
"Led migration of microservices to Azure Kubernetes Service"

Known related-but-NOT-equivalent tools, technologies, or
standards detected: azure

Result:
adjacent

NOT partial, NOT strong, NOT missing. Your reasoning must state
that this is cloud-platform-adjacent experience, not evidence
of AWS itself. The same logic applies across any category —
CRM platforms, accounting standards, container orchestrators,
frontend frameworks, etc.

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
a PARTIAL match when it genuinely overlaps with the exact
required skill but does not prove it. "partial" is reserved
for weaker/incomplete evidence of the SAME required skill —
it must NOT be used for cross-technology adjacency (that is
rule 3a's "adjacent" decision instead).

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
exact or near-exact excerpt from either that requirement's own
"Allowed resume evidence" block OR the "COMPLETE RESUME
EVIDENCE" section. Do not paraphrase, combine, or invent
evidence. Quote only the shortest phrase (roughly 5-20 words)
that proves the point — never the surrounding sentence. If you
cannot quote real evidence from one of these two sources, do
not claim support. This applies to "adjacent" decisions too —
the cited evidence must be real text from one of these two
sources, not an invented technology mention.

14. Do not rewrite or improve the resume.

15. Do not suggest adding anything.

16. If the evidence is insufficient, say so — use decision
"missing" rather than stretching a weak signal into
"partial", "adjacent", or "strong".

17. Confidence represents confidence in the decision,
NOT how impressive the candidate is.

18. unsupported_assumptions must explicitly identify
any assumption that would be required to classify
the candidate more strongly.

19. Evaluate each requirement independently. Having access to
the complete resume evidence does NOT mean evidence found
relevant for one requirement can be reused to justify a
different, unrelated requirement — every piece of cited
evidence must be genuinely and specifically relevant to the
requirement it is cited for.

Return ONLY structured data matching the requested schema,
with exactly one verification per requirement listed above.
"""

        response = api_key_manager.generate_content(
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SemanticVerificationBatch,
                temperature=0.0,
            ),
            purpose=(
                f"semantic_verification_batch_chunk_"
                f"{chunk_index}_of_{total_chunks}"
            ),
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

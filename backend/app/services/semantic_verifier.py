import json
from google.genai import types

from app.core.config import GEMINI_MODEL

from app.services.api_key_manager import (
    api_key_manager,
)
from app.schemas.resume_analysis import (
    JDRequirement,
    ResumeProfile,
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
    """

    def verify_batch(
        self,
        requirements: list[JDRequirement],
        resume_profile: ResumeProfile,
    ) -> dict[str, SemanticVerification]:

        if not requirements:
            return {}

        evidence_context = (
            self._build_evidence_context(
                resume_profile
            )
        )

        requirement_blocks = []

        for index, requirement in enumerate(
            requirements,
            start=1,
        ):
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

JOB DESCRIPTION REQUIREMENTS
=============================

{"".join(requirement_blocks)}


CANDIDATE RESUME EVIDENCE
=========================

{evidence_context}


STRICT RULES
============

1. You may ONLY use information present in the
candidate resume evidence provided above.

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

13. Every supporting evidence item MUST come directly
from the provided resume evidence.

14. Do not rewrite or improve the resume.

15. Do not suggest adding anything.

16. If evidence is insufficient, say so.

17. Confidence represents confidence in the decision,
NOT how impressive the candidate is.

18. unsupported_assumptions must explicitly identify
any assumption that would be required to classify
the candidate more strongly.

19. Evaluate each requirement independently. Evidence
that supports one requirement must not be reused to
justify a different, unrelated requirement.

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

    @staticmethod
    def _build_evidence_context(
        resume_profile: ResumeProfile,
    ) -> str:

        evidence = []

        for item in resume_profile.evidence:

            evidence.append(
                f"""
Section: {item.section}
Claim: {item.claim}
Source: {item.source_text}
Confidence: {item.confidence}
"""
            )

        for skill in resume_profile.skills:

            for item in skill.evidence:

                evidence.append(
                    f"""
Skill: {skill.name}
Section: {item.section}
Claim: {item.claim}
Source: {item.source_text}
Confidence: {item.confidence}
"""
                )

        for project in resume_profile.projects:

            for bullet in project.bullets:

                evidence.append(
                    f"""
Project: {project.name}
Section: projects
Source: {bullet.text}
Technologies: {bullet.technologies}
Metrics: {[m.value for m in bullet.metrics]}
"""
                )

        for experience in resume_profile.experience:

            for bullet in experience.bullets:

                evidence.append(
                    f"""
Experience: {experience.role}
Company: {experience.company}
Section: experience
Source: {bullet.text}
Technologies: {bullet.technologies}
Metrics: {[m.value for m in bullet.metrics]}
"""
                )

        if not evidence:
            return "No usable resume evidence was extracted."

        return "\n".join(evidence)

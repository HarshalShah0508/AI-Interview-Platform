import json

from google.genai import types

from app.core.config import GEMINI_MODEL

from app.services.api_key_manager import (
    api_key_manager,
)
from app.services.requirement_matcher import (
    RequirementMatcher,
)
from app.schemas.resume_analysis import (
    JDProfile,
    JDRequirement,
    ResumeProfile,
    MatchingReport,
    OptimizationReport,
    RecommendationChange,
    KeepAsIs,
    MissingRequirementRecommendation,
    RecommendationDraft,
    RecommendationReport,
)


class RecommendationEngine:
    """
    Generates truth-safe resume recommendations.

    Gemini is only responsible for wording.

    The candidate's existing resume evidence is the
    only permitted source of factual claims.
    """

    def __init__(self):

        # Reused only for its deterministic, Gemini-free
        # component decomposition and controlled concept ->
        # evidence-keyword mapping, so missing-requirement
        # guidance stays consistent with how the matcher
        # itself reasons about a requirement. Constructing
        # this does not make any Gemini calls.
        self._requirement_matcher = RequirementMatcher()

    def generate(
    self,
    jd_profile: JDProfile,
    resume_profile: ResumeProfile,
    matching_report: MatchingReport,
    optimization_report: OptimizationReport,
) -> RecommendationReport:

        recommendations = []

        keep_as_is = []

        missing_actions = []

    # ----------------------------------------------------
    # 1. Generate ALL rewrite recommendations in ONE
    #    Gemini request.
    # ----------------------------------------------------

        findings = [
            finding
            for finding in optimization_report.findings
            if finding.safe_to_rewrite
        ]

        if findings:

            drafts = self._generate_batch_recommendations(
                findings=findings,
                jd_profile=jd_profile,
                resume_profile=resume_profile,
                matching_report=matching_report,
            )

            for draft in drafts:

                validated = (
                    self._validate_draft(
                        draft=draft,
                        resume_profile=resume_profile,
                    )
                )

                if validated is None:
                    continue

                recommendations.append(
                    validated
                )

    # ----------------------------------------------------
    # 2. Strong bullets that should remain unchanged.
    # ----------------------------------------------------

        for bullet in optimization_report.bullet_quality:

            if bullet.overall_score < 85:
                continue

            keep_as_is.append(
                KeepAsIs(
                    original_text=bullet.text,
                    section=bullet.section,
                    reason=(
                        "This bullet already demonstrates "
                        "strong structure, specificity, "
                        "impact and/or JD relevance. "
                        "An unnecessary rewrite may add "
                        "risk without meaningful benefit."
                    ),
                    supporting_evidence=[
                        bullet.text
                    ],
                )
            )

    # ----------------------------------------------------
    # 3. Missing requirements remain deterministic.
    # ----------------------------------------------------

        requirements_by_name = {
            requirement.name: requirement
            for requirement in jd_profile.requirements
        }

        for match in matching_report.matches:

            if match.match_type != "missing":
                continue

            requirement = requirements_by_name.get(
                match.requirement
            )

            missing_actions.append(
                self._missing_requirement_action(
                    match,
                    requirement,
                )
            )

        high_priority = sum(
        1
        for finding in optimization_report.findings
        if finding.priority in {
            "critical",
            "high",
        }
    )

        medium_priority = sum(
        1
        for finding in optimization_report.findings
        if finding.priority == "medium"
    )

        return RecommendationReport(
        recommendations=recommendations,
        keep_as_is=keep_as_is,
        missing_requirement_actions=missing_actions,
        safety_rejected_count=(
            len(findings) - len(recommendations)
            if findings
            else 0
        ),
        high_priority_count=high_priority,
        medium_priority_count=medium_priority,
    )

    # ========================================================
    # Generate recommendation for one finding
    # ========================================================

    def _generate_batch_recommendations(
        self,
        findings,
        jd_profile,
        resume_profile,
        matching_report,
    ) -> list[RecommendationDraft]:
        finding_context = []

        for index, finding in enumerate(
            findings,
            start=1,
        ):
            requirement_context = ""

            if finding.jd_requirement:
                requirement_context = (
                    self._find_requirement_context(
                        finding.jd_requirement,
                        jd_profile,
                        matching_report,
                    )
                )

            evidence_context = (
                self._build_evidence_context(
                    finding,
                    resume_profile,
                )
            )

            finding_context.append(
                f"""
FINDING #{index}

Original text:
{finding.original_text}

Section:
{finding.section}

Finding type:
{finding.finding_type}

Priority:
{finding.priority}

Explanation:
{finding.explanation}

JD requirement:
{finding.jd_requirement or "None"}

JD requirement context:
{requirement_context}

Verified evidence specifically associated
with this finding:
{evidence_context}
"""
            )

        full_resume_evidence = (
            self._build_full_resume_evidence(
                resume_profile
            )
        )

        prompt = f"""
You are the Resume Recommendation Engine for HotSeat.

You are generating conservative rewrite suggestions
for an existing resume.

Your task is NOT to make the candidate appear more
qualified than they actually are.

Your task is to improve:
- clarity
- wording
- specificity
- impact
- JD alignment
- visibility of already-supported skills

WITHOUT changing the factual meaning of the resume.

==================================================
VERIFIED RESUME EVIDENCE
==================================================

{full_resume_evidence}

==================================================
OPTIMIZATION FINDINGS
==================================================

{"".join(finding_context)}

==================================================
ABSOLUTE TRUTH RULES
==================================================

The resume evidence above is the ONLY source of
candidate facts.

NEVER invent:

- technologies
- frameworks
- programming languages
- databases
- cloud platforms
- companies
- job titles
- responsibilities
- achievements
- leadership
- ownership
- production experience
- scale
- users
- rankings
- percentages
- accuracy values
- performance improvements
- dates
- years of experience
- metrics of any kind

A technology may only be mentioned if supported
by the verified resume evidence.

A metric may only be used if the exact metric is
already present in the evidence.

If the original bullet says "worked with X",
do not turn it into "led X".

If the original bullet says "used X",
do not turn it into "architected X".

If the evidence says "improved performance",
do not invent a percentage.

If a useful metric is missing, do NOT add one.

Instead, explain that a verified metric could
strengthen the bullet if the candidate genuinely
has one.

==================================================
EVIDENCE REQUIREMENT
==================================================

For every recommendation:

1. "evidence_used" MUST contain exact excerpts
   from the verified resume evidence.

2. "verified_facts_used" MUST contain only facts
   explicitly supported by the evidence.

3. "added_facts" MUST list every factual element
   introduced by the suggested wording.

4. If a factual element cannot be supported,
   do NOT introduce it.

5. "metric_added" must only be true when the metric
   already exists in the verified evidence.

6. "metric_source" must identify the evidence
   containing that metric.

==================================================
CONSERVATIVE BEHAVIOR
==================================================

If a bullet cannot be safely improved:

Return the original wording.

Do not force a rewrite.

Do not add generic ATS keywords merely because
they appear in the JD.

==================================================
OUTPUT
==================================================

Return ONLY a JSON object matching:

{{
    "recommendations": [
        RecommendationDraft
    ]
}}

Do not return safety_status.

Do not return confidence.

Those will be calculated independently by HotSeat.

Do not return explanations outside the JSON object.
"""

        response = api_key_manager.generate_content(
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
            purpose="batched_recommendations",
        )

        raw = (
            response.text or ""
        ).strip()

        if not raw:
            return []

        try:
            parsed = json.loads(raw)

            drafts = parsed.get(
                "recommendations",
                [],
            )

            return [
                RecommendationDraft.model_validate(
                    item
                )
                for item in drafts
            ]

        except Exception as exc:
            print(
                "[RecommendationEngine] "
                f"Failed to parse batch recommendations: "
                f"{exc}"
            )

            return []

    def _validate_draft(
        self,
        draft: RecommendationDraft,
        resume_profile: ResumeProfile,
    ) -> RecommendationChange | None:
        verified_text = (
            self._build_full_resume_evidence(
                resume_profile
            )
        )

        original = draft.original_text.strip()
        suggested = draft.suggested_text.strip()

        if not original or not suggested:
            return None

        # ----------------------------------------------------
        # The original text must actually exist in the
        # candidate's resume evidence.
        # ----------------------------------------------------

        if not self._fact_exists(
            original,
            verified_text,
        ):
            return None

        # ----------------------------------------------------
        # Every evidence item claimed by Gemini must actually
        # exist in the verified resume.
        # ----------------------------------------------------

        for evidence in draft.evidence_used:
            if not self._fact_exists(
                evidence,
                verified_text,
            ):
                return None

        # ----------------------------------------------------
        # Every explicitly added fact must be independently
        # verified.
        # ----------------------------------------------------

        for fact in draft.added_facts:
            if not self._fact_exists(
                fact,
                verified_text,
            ):
                return None

        # ----------------------------------------------------
        # Metric validation.
        # ----------------------------------------------------

        if draft.metric_added:
            if not draft.metric_source:
                return None

            if not self._fact_exists(
                draft.metric_source,
                verified_text,
            ):
                return None

        # ----------------------------------------------------
        # Numeric validation.
        # ----------------------------------------------------

        original_numbers = (
            self._extract_numbers(
                original
            )
        )

        suggested_numbers = (
            self._extract_numbers(
                suggested
            )
        )

        resume_numbers = (
            self._extract_numbers(
                verified_text
            )
        )

        new_numbers = (
            suggested_numbers
            - original_numbers
        )

        unsupported_numbers = (
            new_numbers
            - resume_numbers
        )

        if unsupported_numbers:
            return None

        # ----------------------------------------------------
        # If Gemini returned unchanged text, don't present
        # it as an improvement.
        # ----------------------------------------------------

        if (
            self._normalize(suggested)
            == self._normalize(original)
        ):
            return RecommendationChange(
                original_text=original,
                suggested_text=suggested,
                change_type=draft.change_type,
                jd_requirement=draft.jd_requirement,
                reason=draft.reason,
                evidence_used=draft.evidence_used,
                verified_facts_used=(
                    draft.verified_facts_used
                ),
                added_facts=draft.added_facts,
                removed_claims=draft.removed_claims,
                metric_added=draft.metric_added,
                metric_source=draft.metric_source,
                safety_status="needs_verification",
                confidence=0.85,
            )

        # ----------------------------------------------------
        # Safe recommendation.
        # ----------------------------------------------------

        confidence = self._calculate_local_confidence(
            draft=draft,
            original=original,
            suggested=suggested,
            verified_text=verified_text,
        )

        if confidence < 0.90:
            safety_status = "needs_verification"
        else:
            safety_status = "safe"

        return RecommendationChange(
            original_text=original,
            suggested_text=suggested,
            change_type=draft.change_type,
            jd_requirement=draft.jd_requirement,
            reason=draft.reason,
            evidence_used=draft.evidence_used,
            verified_facts_used=(
                draft.verified_facts_used
            ),
            added_facts=draft.added_facts,
            removed_claims=draft.removed_claims,
            metric_added=draft.metric_added,
            metric_source=draft.metric_source,
            safety_status=safety_status,
            confidence=confidence,
        )

    def _calculate_local_confidence(
        self,
        draft: RecommendationDraft,
        original: str,
        suggested: str,
        verified_text: str,
    ) -> float:
        score = 1.0

        # Evidence must exist.
        if not draft.evidence_used:
            score -= 0.20

        # Facts claimed by Gemini must be verifiable.
        for fact in draft.verified_facts_used:
            if not self._fact_exists(
                fact,
                verified_text,
            ):
                score -= 0.30

        # Any declared additions are risky.
        if draft.added_facts:
            score -= 0.10

        # Metrics receive extra scrutiny.
        if draft.metric_added:
            score -= 0.05

        # Removing claims can alter meaning.
        if draft.removed_claims:
            score -= 0.05

        # Large wording changes deserve more caution.
        original_words = set(
            self._normalize(original).split()
        )

        suggested_words = set(
            self._normalize(suggested).split()
        )

        if original_words:
            changed_ratio = (
                len(
                    suggested_words
                    - original_words
                )
                / len(original_words)
            )

            if changed_ratio > 0.50:
                score -= 0.10

        return max(
            0.0,
            min(
                score,
                1.0,
            ),
        )

    # ========================================================
    # Missing requirement handling
    # ========================================================

    def _missing_requirement_action(
        self,
        match,
        requirement: JDRequirement | None,
    ) -> MissingRequirementRecommendation:

        evidence_hint = self._missing_requirement_evidence_hint(
            match,
            requirement,
        )

        if match.importance == "required":

            action = "verify_experience"

            warning = (
                "Do not add this requirement merely because "
                "it appears in the JD. Review your projects, "
                f"internships, and coursework for {evidence_hint}. "
                "If you genuinely have this experience, surface "
                "it explicitly in the relevant bullet. If you do "
                "not, do not add it."
            )

        elif match.importance == "preferred":

            action = "add_if_true"

            warning = (
                "This is preferred by the JD, not required. "
                f"Review your background for {evidence_hint}. "
                "Only mention it if it is genuinely true — do "
                "not add it merely because the JD lists it."
            )

        else:

            action = "do_not_add"

            warning = (
                "There is currently insufficient evidence to "
                f"justify adding this. If you have real experience "
                f"with {evidence_hint}, you may add it truthfully; "
                "otherwise leave your resume as-is."
            )

        return MissingRequirementRecommendation(
            requirement=match.requirement,
            importance=match.importance,
            reason=match.reason,
            candidate_action=action,
            warning=warning,
        )

    def _missing_requirement_evidence_hint(
        self,
        match,
        requirement: JDRequirement | None,
    ) -> str:
        """
        Builds a concrete "what to look for" hint for a missing
        requirement, using the same deterministic component
        decomposition and controlled concept -> evidence-keyword
        mapping the matcher itself uses — entirely local, no
        Gemini call involved.
        """

        if requirement is None:
            return match.requirement

        components = (
            self._requirement_matcher._resolve_components(
                requirement
            )
        )

        hint_terms: set[str] = set()

        for component in components:

            hint_terms.update(
                self._requirement_matcher._concept_hint_terms(
                    component
                )
            )

        if hint_terms:

            sample = sorted(hint_terms)[:6]

            return ", ".join(sample)

        if len(components) > 1:

            return ", ".join(components)

        if requirement.aliases:

            return ", ".join(
                dict.fromkeys(
                    [requirement.name, *requirement.aliases]
                )
            )

        return requirement.name

    # ========================================================
    # Evidence context
    # ========================================================

    def _build_evidence_context(
        self,
        finding,
        resume_profile,
    ) -> str:

        evidence = []

        for item in finding.evidence:

            evidence.append(
                f"- {item}"
            )

        if not evidence:

            evidence.append(
                "- No additional evidence available."
            )

        return "\n".join(
            evidence
        )

    def _build_full_resume_evidence(
        self,
        resume_profile,
    ) -> str:

        evidence = []

        for item in resume_profile.evidence:

            evidence.append(
                item.source_text
            )

        for skill in resume_profile.skills:

            evidence.append(
                skill.name
            )

            for item in skill.evidence:

                evidence.append(
                    item.source_text
                )

        for project in resume_profile.projects:

            for bullet in project.bullets:

                evidence.append(
                    bullet.text
                )

        for experience in resume_profile.experience:

            for bullet in experience.bullets:

                evidence.append(
                    bullet.text
                )

        return "\n".join(
            evidence
        )

    # ========================================================
    # Requirement context
    # ========================================================

    def _find_requirement_context(
        self,
        requirement_name,
        jd_profile,
        matching_report,
    ) -> str:

        requirement = None

        for item in jd_profile.requirements:

            if (
                item.name.lower()
                == requirement_name.lower()
            ):

                requirement = item
                break

        match = None

        for item in matching_report.matches:

            if (
                item.requirement.lower()
                == requirement_name.lower()
            ):

                match = item
                break

        if not requirement:

            return (
                f"JD requirement: "
                f"{requirement_name}"
            )

        result = [
            f"Requirement: {requirement.name}",
            f"Category: {requirement.category}",
            f"Importance: {requirement.importance}",
            f"Weight: {requirement.weight}",
        ]

        if requirement.evidence:

            result.append(
                "JD evidence:"
            )

            result.extend(
                f"- {item}"
                for item in requirement.evidence
            )

        if match:

            result.extend(
                [
                    "",
                    f"Current match: {match.match_type}",
                    f"Match score: {match.score}",
                    f"Reason: {match.reason}",
                ]
            )

        return "\n".join(
            result
        )

    # ========================================================
    # Helpers
    # ========================================================

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:

        return " ".join(
            text.lower().split()
        )

    def _fact_exists(
        self,
        fact: str,
        evidence: str,
    ) -> bool:

        normalized_fact = self._normalize(
            fact
        )

        normalized_evidence = self._normalize(
            evidence
        )

        return (
            normalized_fact
            in normalized_evidence
        )
    
    def _extract_numbers(
        self,
        text: str,
    ) -> set[str]:

        import re

        return set(
            re.findall(
                r"\b\d+(?:\.\d+)?%?\b",
                text,
            )
        )

import re
from difflib import SequenceMatcher

from app.schemas.resume_analysis import (
    JDProfile,
    JDRequirement,
    RequirementMatch,
    MatchingReport,
    MatchingSummary,
    ResumeProfile,
    ResumeEvidence,
)
from app.services.semantic_verifier import (
    SemanticVerifier,
)

class RequirementMatcher:
    """
    Deterministic Resume ↔ JD matching engine.

    The matcher deliberately does NOT let an LLM
    arbitrarily decide the score.

    Matching is based on:

    1. Exact matches
    2. Controlled aliases
    3. Evidence context
    4. Conservative fuzzy matching
    5. Requirement importance
    6. Evidence confidence
    """
    def __init__(self):
        self.semantic_verifier = SemanticVerifier()
    # --------------------------------------------------------
    # Controlled aliases
    # --------------------------------------------------------

    COMMON_ALIASES = {
        "postgres": {
            "postgresql",
        },

        "postgresql": {
            "postgres",
        },

        "restful api": {
            "rest api",
            "rest apis",
            "restful apis",
        },

        "rest api": {
            "restful api",
            "rest apis",
            "restful apis",
        },

        "javascript": {
            "js",
            "ecmascript",
        },

        "typescript": {
            "ts",
        },

        "cplusplus": {
            "c++",
            "cpp",
        },

        "c++": {
            "cplusplus",
            "cpp",
        },

        "kubernetes": {
            "k8s",
        },

        "ci/cd": {
            "cicd",
            "continuous integration",
            "continuous deployment",
            "continuous integration and deployment",
        },

        "machine learning": {
            "ml",
        },

        "artificial intelligence": {
            "ai",
        },

        "application programming interface": {
            "api",
            "apis",
        },
    }

    # --------------------------------------------------------
    # Important: these must NEVER be treated as aliases.
    # --------------------------------------------------------

    INCOMPATIBLE_TECHNOLOGIES = {
        frozenset(("aws", "azure")),
        frozenset(("aws", "gcp")),
        frozenset(("azure", "gcp")),
        frozenset(("docker", "kubernetes")),
        frozenset(("react", "angular")),
        frozenset(("react", "vue")),
        frozenset(("python", "java")),
        frozenset(("postgresql", "mysql")),
        frozenset(("postgres", "mysql")),
    }

    IMPORTANCE_MULTIPLIERS = {
        "required": 1.00,
        "preferred": 0.70,
        "nice_to_have": 0.50,
        "unclear": 0.50,
    }
    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def match(
    self,
    jd_profile: JDProfile,
    resume_profile: ResumeProfile,
) -> MatchingReport:

        results: list[RequirementMatch] = []

        for requirement in jd_profile.requirements:

            result = self._match_requirement(
               requirement,
               resume_profile,
            )

        # ----------------------------------------------------
        # Semantic verification is ONLY used for ambiguous
        # deterministic results.
        # ----------------------------------------------------

            if result.match_type == "ambiguous":

                result = self._verify_ambiguous_match(
                    requirement,
                    resume_profile,
                    result,
              )

            results.append(result)

        overall_score = self._calculate_overall_score(
            results
        )

        summary = self._build_summary(
            results
        )

        return MatchingReport(
            overall_score=round(
                overall_score,
                2,
            ),
            summary=summary,
            matches=results,
        )

    # --------------------------------------------------------
    # Requirement matching
    # --------------------------------------------------------

    def _match_requirement(
        self,
        requirement: JDRequirement,
        resume_profile: ResumeProfile,
    ) -> RequirementMatch:

        requirement_name = self._normalize(
            requirement.name
        )

        aliases = set(
            self._normalize(alias)
            for alias in requirement.aliases
        )

        aliases.update(
            self.COMMON_ALIASES.get(
                requirement_name,
                set(),
            )
        )

        candidate_terms = {
            requirement_name,
            *aliases,
        }

        evidence = self._find_evidence(
            candidate_terms,
            resume_profile,
        )

        # ----------------------------------------------------
        # No evidence
        # ----------------------------------------------------

        if not evidence:

            return RequirementMatch(
                requirement=requirement.name,
                category=requirement.category,
                importance=requirement.importance,
                weight=requirement.weight,
                match_type="missing",
                match_strength=0.0,
                evidence_confidence=0.0,
                score=0.0,
                matched_resume_evidence=[],
                matched_resume_sections=[],
                reason=(
                    "No direct or controlled-alias "
                    "evidence for this requirement "
                    "was found in the resume."
                ),
                aliases_considered=sorted(
                    aliases
                ),
            )

        # ----------------------------------------------------
        # Evaluate evidence
        # ----------------------------------------------------

        best_evidence = max(
            evidence,
            key=lambda item: item["strength"],
        )

        strength = best_evidence["strength"]

        confidence = max(
            item["confidence"]
            for item in evidence
        )

        matched_evidence = list(
            dict.fromkeys(
                item["source_text"]
                for item in evidence
            )
        )

        matched_sections = list(
            dict.fromkeys(
                item["section"]
                for item in evidence
            )
        )

        match_type = self._classify_match(
            strength,
            confidence,
        )

        score = (
            strength
            * confidence
            * 100
        )

        reason = self._build_reason(
            requirement,
            match_type,
            best_evidence,
        )

        return RequirementMatch(
            requirement=requirement.name,
            category=requirement.category,
            importance=requirement.importance,
            weight=requirement.weight,
            match_type=match_type,
            match_strength=round(
                strength,
                3,
            ),
            evidence_confidence=round(
                confidence,
                3,
            ),
            score=round(
                score,
                2,
            ),
            matched_resume_evidence=matched_evidence,
            matched_resume_sections=matched_sections,
            reason=reason,
            aliases_considered=sorted(
                aliases
            ),
        )

    # --------------------------------------------------------
    # Evidence search
    # --------------------------------------------------------

    def _find_evidence(
        self,
        candidate_terms: set[str],
        resume_profile: ResumeProfile,
    ) -> list[dict]:

        results = []

        all_evidence = list(
            resume_profile.evidence
        )

        for skill in resume_profile.skills:

            all_evidence.extend(
                skill.evidence
            )

        for experience in resume_profile.experience:

            for bullet in experience.bullets:

                all_evidence.append(
                    ResumeEvidence(
                        claim=bullet.text,
                        category="responsibility",
                        source_text=bullet.text,
                        section="experience",
                        confidence=0.90,
                    )
                )

        for project in resume_profile.projects:

            for bullet in project.bullets:

                all_evidence.append(
                    ResumeEvidence(
                        claim=bullet.text,
                        category="project",
                        source_text=bullet.text,
                        section="projects",
                        confidence=0.90,
                    )
                )

        for evidence in all_evidence:

            source = self._normalize(
                evidence.source_text
            )

            claim = self._normalize(
                evidence.claim
            )

            strength = self._calculate_match_strength(
                candidate_terms,
                source,
                claim,
            )

            if strength > 0:

                results.append(
                    {
                        "strength": strength,
                        "confidence": evidence.confidence,
                        "source_text": evidence.source_text,
                        "section": evidence.section,
                    }
                )

        return results

    # --------------------------------------------------------
    # Match strength
    # --------------------------------------------------------

    def _calculate_match_strength(
        self,
        candidate_terms: set[str],
        source_text: str,
        claim: str,
    ) -> float:

        # ----------------------------------------------------
        # Exact phrase match
        # ----------------------------------------------------

        for term in candidate_terms:

            if not term:
                continue

            if self._contains_phrase(
                source_text,
                term,
            ):
                return 1.0

            if self._contains_phrase(
                claim,
                term,
            ):
                return 1.0

        # ----------------------------------------------------
        # Token-based matching
        # ----------------------------------------------------

        source_tokens = set(
            self._tokenize(source_text)
        )

        claim_tokens = set(
            self._tokenize(claim)
        )

        best_similarity = 0.0

        for term in candidate_terms:

            term_tokens = set(
                self._tokenize(term)
            )

            if not term_tokens:
                continue

            source_overlap = (
                len(
                    term_tokens
                    & source_tokens
                )
                / len(term_tokens)
            )

            claim_overlap = (
                len(
                    term_tokens
                    & claim_tokens
                )
                / len(term_tokens)
            )

            overlap = max(
                source_overlap,
                claim_overlap,
            )

            best_similarity = max(
                best_similarity,
                overlap,
            )

        # ----------------------------------------------------
        # Conservative fuzzy matching
        # ----------------------------------------------------

        if best_similarity >= 0.8:

            return 0.70

        if best_similarity >= 0.5:

            return 0.45

        return 0.0

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    def _classify_match(
        self,
        strength: float,
        confidence: float,
    ) -> str:

        combined = (
            strength
            * confidence
        )

        if combined >= 0.80:

            return "strong"

        if combined >= 0.45:

            return "partial"

        if combined > 0:

            return "ambiguous"

        return "missing"

    # --------------------------------------------------------
    # Overall score
    # --------------------------------------------------------

    def _calculate_overall_score(
        self,
        results: list[RequirementMatch],
    ) -> float:

        if not results:
            return 0.0

        weighted_score = 0.0
        total_weight = 0.0

        for result in results:

            importance_multiplier = (
                self.IMPORTANCE_MULTIPLIERS.get(
                    result.importance,
                    0.50,
                )
            )

            effective_weight = (
                result.weight
                * importance_multiplier
            )

            weighted_score += (
                result.match_strength
                * result.evidence_confidence
                * effective_weight
            )

            total_weight += effective_weight

        if total_weight == 0:

            return 0.0

        return (
            weighted_score
            / total_weight
        ) * 100

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    def _build_summary(
        self,
        results: list[RequirementMatch],
    ) -> MatchingSummary:

        strong = sum(
            1
            for result in results
            if result.match_type == "strong"
        )

        partial = sum(
            1
            for result in results
            if result.match_type == "partial"
        )

        ambiguous = sum(
            1
            for result in results
            if result.match_type == "ambiguous"
        )

        missing = sum(
            1
            for result in results
            if result.match_type == "missing"
        )

        required_results = [
            result
            for result in results
            if result.importance == "required"
        ]

        preferred_results = [
            result
            for result in results
            if result.importance == "preferred"
        ]

        required_matched = sum(
            1
            for result in required_results
            if result.match_type == "strong"
        )

        preferred_matched = sum(
            1
            for result in preferred_results
            if result.match_type == "strong"
        )

        return MatchingSummary(
            total_requirements=len(
                results
            ),
            strong_matches=strong,
            partial_matches=partial,
            ambiguous_matches=ambiguous,
            missing_matches=missing,
            required_requirements=len(
                required_results
            ),
            required_matched=required_matched,
            preferred_requirements=len(
                preferred_results
            ),
            preferred_matched=preferred_matched,
        )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    def _build_reason(
        self,
        requirement: JDRequirement,
        match_type: str,
        evidence: dict,
    ) -> str:

        if match_type == "strong":

            return (
                f"The resume contains strong evidence "
                f"for {requirement.name}. "
                f"The evidence appears in the "
                f"{evidence['section']} section."
            )

        if match_type == "partial":

            return (
                f"The resume contains some evidence "
                f"related to {requirement.name}, "
                f"but the evidence is not strong enough "
                f"to classify it as a strong match."
            )

        if match_type == "ambiguous":

            return (
                f"The resume contains potentially "
                f"related evidence for {requirement.name}, "
                f"but it is not sufficiently explicit."
            )

        return (
            f"No reliable evidence for "
            f"{requirement.name} was found."
        )

    # --------------------------------------------------------
    # Text utilities
    # --------------------------------------------------------

    @staticmethod
    def _normalize(text: str) -> str:

        text = text.lower().strip()

        text = (
            text
            .replace("–", "-")
            .replace("—", "-")
            .replace("_", " ")
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text

    @staticmethod
    def _tokenize(text: str) -> list[str]:

        return re.findall(
            r"[a-z0-9+#./-]+",
            text.lower(),
        )

    @staticmethod
    def _contains_phrase(
        text: str,
        phrase: str,
    ) -> bool:

        text = text.lower()
        phrase = phrase.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)"
        )

        return bool(
            re.search(
                pattern,
                text,
            )
        )
    def _verify_ambiguous_match(
        self,
        requirement: JDRequirement,
        resume_profile: ResumeProfile,
        preliminary_result: RequirementMatch,
    ) -> RequirementMatch:
        verification = (
            self.semantic_verifier.verify(
                requirement=requirement,
                resume_profile=resume_profile,
            )
        )

        # --------------------------------------------------------
        # Safety rule:
        #
        # Gemini cannot promote a requirement to STRONG unless
        # it actually provides supporting evidence.
        # --------------------------------------------------------

        supporting_evidence = (
            verification.supporting_evidence
        )

        if not supporting_evidence:

            return RequirementMatch(
                requirement=requirement.name,
                category=requirement.category,
                importance=requirement.importance,
                weight=requirement.weight,
                match_type="missing",
                match_strength=0.0,
                evidence_confidence=0.0,
                score=0.0,
                matched_resume_evidence=[],
                matched_resume_sections=[],
                reason=(
                    "The resume contains potentially related "
                    "information, but there is insufficient "
                    "evidence to establish this requirement."
                ),
                aliases_considered=(
                    preliminary_result.aliases_considered
                ),
            )

        # --------------------------------------------------------
        # Conservative semantic strength
        # --------------------------------------------------------

        if verification.decision == "strong":

            strength = min(
                0.90,
                verification.confidence,
            )

            match_type = "strong"

        elif verification.decision == "partial":

            strength = min(
                0.65,
                verification.confidence,
            )

            match_type = "partial"

        elif verification.decision == "missing":

            strength = 0.0
            match_type = "missing"

        else:

            strength = min(
                0.40,
                verification.confidence,
            )

            match_type = "ambiguous"

        score = (
            strength
            * verification.confidence
            * 100
        )

        return RequirementMatch(
            requirement=requirement.name,
            category=requirement.category,
            importance=requirement.importance,
            weight=requirement.weight,
            match_type=match_type,
            match_strength=round(
                strength,
                3,
            ),
            evidence_confidence=round(
                verification.confidence,
                3,
            ),
            score=round(
                score,
                2,
            ),
            matched_resume_evidence=(
                supporting_evidence
            ),
            matched_resume_sections=[],
            reason=verification.reasoning,
            aliases_considered=(
                preliminary_result.aliases_considered
            ),
        )

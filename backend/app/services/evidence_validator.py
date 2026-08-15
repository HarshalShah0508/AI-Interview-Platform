import re

from app.schemas.resume_analysis import (
    ResumeProfile,
)


class EvidenceValidator:
    """
    Validates that structured resume evidence is
    actually grounded in the original resume text.
    """

    def validate(
        self,
        resume_text: str,
        profile: ResumeProfile,
    ) -> ResumeProfile:

        normalized_resume = self._normalize(
            resume_text
        )

        # ----------------------------------------------------
        # Validate general evidence
        # ----------------------------------------------------

        valid_evidence = []

        for evidence in profile.evidence:

            if self._is_supported(
                evidence.source_text,
                normalized_resume,
            ):
                valid_evidence.append(
                    evidence
                )

        profile.evidence = valid_evidence

        # ----------------------------------------------------
        # Validate skills
        # ----------------------------------------------------

        valid_skills = []

        for skill in profile.skills:

            valid_skill_evidence = []

            for evidence in skill.evidence:

                if not self._is_supported(
                    evidence.source_text,
                    normalized_resume,
                ):
                    continue

                # Technology itself should either appear
                # in the evidence or have a valid contextual
                # source.
                if not self._term_supported(
                    skill.name,
                    evidence.source_text,
                ):
                    continue

                valid_skill_evidence.append(
                    evidence
                )

            if valid_skill_evidence:

                skill.evidence = (
                    valid_skill_evidence
                )

                valid_skills.append(
                    skill
                )

        profile.skills = valid_skills

        # ----------------------------------------------------
        # Validate project bullets
        # ----------------------------------------------------

        for project in profile.projects:

            valid_bullets = []

            for bullet in project.bullets:

                if not self._is_supported(
                    bullet.text,
                    normalized_resume,
                ):
                    continue

                valid_bullets.append(
                    bullet
                )

            project.bullets = valid_bullets

        # ----------------------------------------------------
        # Validate experience bullets
        # ----------------------------------------------------

        for experience in profile.experience:

            valid_bullets = []

            for bullet in experience.bullets:

                if not self._is_supported(
                    bullet.text,
                    normalized_resume,
                ):
                    continue

                valid_bullets.append(
                    bullet
                )

            experience.bullets = valid_bullets

        return profile

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:

        text = text.lower()

        text = (
            text
            .replace("–", "-")
            .replace("—", "-")
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def _is_supported(
        self,
        source_text: str,
        normalized_resume: str,
    ) -> bool:

        normalized_source = self._normalize(
            source_text
        )

        if not normalized_source:
            return False

        # Exact source substring.
        if normalized_source in normalized_resume:
            return True

        # Sometimes whitespace or punctuation differs.
        source_tokens = self._tokenize(
            normalized_source
        )

        resume_tokens = self._tokenize(
            normalized_resume
        )

        if not source_tokens:
            return False

        # At least 85% of source words should be
        # represented in the original resume.
        overlap = sum(
            1
            for token in source_tokens
            if token in resume_tokens
        )

        ratio = (
            overlap
            / len(source_tokens)
        )

        return ratio >= 0.85

    def _term_supported(
        self,
        term: str,
        source_text: str,
    ) -> bool:

        normalized_term = self._normalize(
            term
        )

        normalized_source = self._normalize(
            source_text
        )

        if normalized_term in normalized_source:
            return True

        # Controlled abbreviation handling.
        aliases = {
            "javascript": {"js"},
            "typescript": {"ts"},
            "postgresql": {"postgres"},
            "cplusplus": {"c++", "cpp"},
            "c++": {"cplusplus", "cpp"},
            "kubernetes": {"k8s"},
            "python": {"python 3"},
        }

        for alias in aliases.get(
            normalized_term,
            set(),
        ):

            if alias in normalized_source:
                return True

        return False

    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:

        return re.findall(
            r"[a-z0-9+#./-]+",
            text.lower(),
        )
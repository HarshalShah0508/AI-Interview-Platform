"""
Role classification service.

This module determines which interview category a selected role belongs to.

Classification Strategy
-----------------------
1. Exact role matching
2. Keyword matching
3. Gemini fallback

Returns exactly one category:

- software
- finance
- consulting
- sales
- marketing
"""


SOFTWARE_KEYWORDS = {
    "software",
    "developer",
    "engineer",
    "backend",
    "frontend",
    "front end",
    "back end",
    "full stack",
    "fullstack",
    "devops",
    "cloud",
    "android",
    "ios",
    "mobile",
    "web",
    "python",
    "java",
    "c++",
    "cpp",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "node",
    "nodejs",
    "django",
    "flask",
    "fastapi",
    "spring",
    "machine learning",
    "ml",
    "artificial intelligence",
    "ai",
    "deep learning",
    "nlp",
    "computer vision",
    "data engineer",
    "data scientist",
    "software engineer",
}

FINANCE_KEYWORDS = {
    "finance",
    "financial",
    "investment",
    "investment banking",
    "banking",
    "equity",
    "private equity",
    "venture capital",
    "portfolio",
    "asset management",
    "wealth management",
    "treasury",
    "valuation",
    "risk",
    "risk management",
    "quant",
    "quantitative",
    "corporate finance",
    "financial analyst",
    "equity research",
    "credit analyst",
}

CONSULTING_KEYWORDS = {
    "consultant",
    "consulting",
    "strategy",
    "strategy consultant",
    "business consulting",
    "management consulting",
    "operations consulting",
    "operations",
    "business analyst",
    "advisory",
    "transformation",
}

SALES_KEYWORDS = {
    "sales",
    "sales executive",
    "sales manager",
    "account manager",
    "account executive",
    "business development",
    "business development executive",
    "relationship manager",
    "customer success",
    "inside sales",
    "enterprise sales",
}

MARKETING_KEYWORDS = {
    "marketing",
    "digital marketing",
    "performance marketing",
    "growth marketing",
    "product marketing",
    "brand",
    "branding",
    "seo",
    "sem",
    "content",
    "content marketing",
    "marketing analyst",
    "marketing manager",
    "growth",
}


class RoleClassifier:
    """
    Determines the interview category for a given role.
    """

    VALID_CATEGORIES = {
        "software",
        "finance",
        "consulting",
        "sales",
        "marketing",
    }

    @staticmethod
    def _normalize_role(role: str) -> str:
        return role.strip().lower()

    def _exact_match(self, role: str) -> str | None:

        role = self._normalize_role(role)

        if role in SOFTWARE_KEYWORDS:
            return "software"

        if role in FINANCE_KEYWORDS:
            return "finance"

        if role in CONSULTING_KEYWORDS:
            return "consulting"

        if role in SALES_KEYWORDS:
            return "sales"

        if role in MARKETING_KEYWORDS:
            return "marketing"

        return None

    def _keyword_match(self, role: str) -> str | None:

        role = self._normalize_role(role)

        for keyword in SOFTWARE_KEYWORDS:
            if keyword in role:
                return "software"

        for keyword in FINANCE_KEYWORDS:
            if keyword in role:
                return "finance"

        for keyword in CONSULTING_KEYWORDS:
            if keyword in role:
                return "consulting"

        for keyword in SALES_KEYWORDS:
            if keyword in role:
                return "sales"

        for keyword in MARKETING_KEYWORDS:
            if keyword in role:
                return "marketing"

        return None

    def _gemini_classification(
        self,
        role: str,
        model,
    ) -> str:
        """
        Uses Gemini only when keyword matching fails.
        """

        prompt = f"""
Classify the following interview role into EXACTLY ONE category.

Categories:
Software
Finance
Consulting
Sales
Marketing

Interview Role:
{role}

Rules:
- Return ONLY one category.
- Do not explain your answer.
- Do not use punctuation.
"""

        response = model.generate_content(prompt)

        category = response.text.strip().lower()

        if category not in self.VALID_CATEGORIES:
            return "software"

        return category

    def classify_role(
        self,
        role: str,
        model,
    ) -> str:
        """
        Determines the interview category.

        Priority:
        1. Exact role match
        2. Keyword match
        3. Gemini fallback
        """

        category = self._exact_match(role)

        if category:
            return category

        category = self._keyword_match(role)

        if category:
            return category

        return self._gemini_classification(
            role=role,
            model=model,
        )
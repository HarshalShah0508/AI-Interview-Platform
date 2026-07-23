"""
Role classification service.

This module determines which interview category a selected role belongs to.

Classification strategy:

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

from app.services.api_key_manager import APIKeyManager


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
    "react",
    "node",
    "machine learning",
    "ml",
    "ai",
    "artificial intelligence",
    "data engineer",
    "data scientist",
}

FINANCE_KEYWORDS = {
    "finance",
    "financial",
    "investment",
    "banking",
    "equity",
    "portfolio",
    "treasury",
    "risk",
    "valuation",
    "quant",
    "analyst",
    "corporate finance",
    "private equity",
    "venture capital",
    "asset management",
    "wealth management",
}

CONSULTING_KEYWORDS = {
    "consultant",
    "consulting",
    "strategy",
    "business consulting",
    "management consulting",
    "operations consulting",
    "operations",
    "advisory",
    "strategy consultant",
}

SALES_KEYWORDS = {
    "sales",
    "business development",
    "account manager",
    "account executive",
    "relationship manager",
    "customer success",
    "sales executive",
    "sales manager",
    "inside sales",
    "enterprise sales",
}

MARKETING_KEYWORDS = {
    "marketing",
    "brand",
    "branding",
    "seo",
    "sem",
    "growth",
    "content",
    "content marketing",
    "digital marketing",
    "performance marketing",
    "product marketing",
    "marketing analyst",
}


class RoleClassifier:
    """
    Classifies interview roles into predefined interview categories.
    """

    def __init__(self):

        self.key_manager = APIKeyManager()

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

    def _gemini_classification(self, role: str) -> str:

        prompt = f"""
Classify the following interview role into exactly ONE category.

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
- Do not explain.
- Do not include punctuation.
"""

        response = self.key_manager.generate_content(prompt)

        category = response.text.strip().lower()

        valid_categories = {
            "software",
            "finance",
            "consulting",
            "sales",
            "marketing",
        }

        if category not in valid_categories:
            return "software"

        return category

    def classify_role(self, role: str) -> str:
        """
        Classify a role into one of the supported interview categories.
        """

        category = self._exact_match(role)

        if category:
            return category

        category = self._keyword_match(role)

        if category:
            return category

        return self._gemini_classification(role)
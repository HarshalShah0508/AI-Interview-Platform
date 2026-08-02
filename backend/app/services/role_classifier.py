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
- digital_design
- analog_design
- embedded_systems
- vlsi
- product_management
"""

from app.services.api_key_manager import APIKeyManager


SOFTWARE_KEYWORDS = {
    "software engineer",
    "software developer",
    "backend engineer",
    "backend developer",
    "frontend engineer",
    "frontend developer",
    "front end engineer",
    "back end engineer",
    "full stack engineer",
    "full stack developer",
    "fullstack developer",
    "web developer",
    "application developer",
    "python developer",
    "java developer",
    "c++ developer",
    "cpp developer",
    "android developer",
    "ios developer",
    "mobile developer",
    "cloud engineer",
    "devops engineer",
    "site reliability engineer",
    "sre",
    "machine learning engineer",
    "ml engineer",
    "ai engineer",
    "artificial intelligence engineer",
    "data engineer",
    "data scientist",
    "sde",
"software development engineer",
"full stack",
"frontend",
"backend",
"web engineer",
"application engineer",
"java engineer",
"python engineer",
"c++ engineer",
"cpp engineer",
"react developer",
"node developer",
"ios engineer",
"android engineer",
}


FINANCE_KEYWORDS = {
    "financial analyst",
    "finance analyst",
    "investment banking",
    "investment banker",
    "investment analyst",
    "equity research",
    "equity analyst",
    "portfolio manager",
    "portfolio analyst",
    "treasury",
    "risk analyst",
    "valuation",
    "corporate finance",
    "private equity",
    "venture capital",
    "asset management",
    "wealth management",
    "credit analyst",
}


CONSULTING_KEYWORDS = {
    "consultant",
    "management consultant",
    "strategy consultant",
    "business consultant",
    "operations consultant",
    "business consulting",
    "management consulting",
    "operations consulting",
    "advisory",
    "business analyst",
}


SALES_KEYWORDS = {
    "sales executive",
    "sales manager",
    "business development",
    "business development representative",
    "sales development representative",
    "account executive",
    "account manager",
    "relationship manager",
    "customer success",
    "inside sales",
    "enterprise sales",
}


MARKETING_KEYWORDS = {
    "marketing",
    "marketing analyst",
    "digital marketing",
    "performance marketing",
    "growth marketing",
    "product marketing",
    "brand manager",
    "branding",
    "seo",
    "sem",
    "content marketing",
}


DIGITAL_DESIGN_KEYWORDS = {
    "rtl",
    "rtl engineer",
    "rtl design",
    "digital design",
    "digital design engineer",
    "asic",
    "asic engineer",
    "asic design engineer",
    "logic design",
    "logic design engineer",
    "verification engineer",
    "design verification",
    "dv engineer",
    "fpga",
    "fpga engineer",
    "fpga design engineer",
    "verilog",
    "systemverilog",
    "rtl developer",
"verification",
"design verification engineer",
}


ANALOG_DESIGN_KEYWORDS = {
    "analog",
    "analog design",
    "analog engineer",
    "analog design engineer",
    "analog ic",
    "analog ic design",
    "analog ic engineer",
    "mixed signal",
    "mixed signal engineer",
    "mixed signal design",
    "circuit design",
}


EMBEDDED_SYSTEMS_KEYWORDS = {
    "embedded",
    "embedded engineer",
    "embedded systems",
    "embedded systems engineer",
    "embedded software",
    "embedded software engineer",
    "firmware",
    "firmware engineer",
    "device driver",
    "device driver engineer",
    "microcontroller",
    "microcontroller engineer",
    "iot",
    "automotive embedded",
    "embedded linux",
"embedded linux engineer",
"linux kernel",
"kernel developer",
}


VLSI_KEYWORDS = {
    "vlsi",
    "physical design",
    "physical design engineer",
    "backend vlsi",
    "backend design",
    "backend engineer",
    "physical verification",
    "timing engineer",
    "sta",
    "static timing",
    "dft",
    "scan",
    "pd engineer",
    "synthesis",
"synthesis engineer",
"physical implementation",
"timing closure",
"physical design",
"backend physical design",
}


PRODUCT_MANAGEMENT_KEYWORDS = {
    "product manager",
    "associate product manager",
    "assistant product manager",
    "apm",
    "technical product manager",
    "group product manager",
    "senior product manager",
    "principal product manager",
    "product owner",
    "product analyst",
    "product management",
    "growth product manager",
    "platform product manager",
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

        if role in DIGITAL_DESIGN_KEYWORDS:
            return "digital_design"

        if role in ANALOG_DESIGN_KEYWORDS:
            return "analog_design"

        if role in EMBEDDED_SYSTEMS_KEYWORDS:
            return "embedded_systems"

        if role in VLSI_KEYWORDS:
            return "vlsi"

        if role in PRODUCT_MANAGEMENT_KEYWORDS:
            return "product_management"

        if role in FINANCE_KEYWORDS:
            return "finance"

        if role in CONSULTING_KEYWORDS:
            return "consulting"

        if role in SALES_KEYWORDS:
            return "sales"

        if role in MARKETING_KEYWORDS:
            return "marketing"

        if role in SOFTWARE_KEYWORDS:
            return "software"

        return None
    def _keyword_match(self, role: str) -> str | None:

        role = self._normalize_role(role)

        # Electronics domains first (more specific)

        for keyword in DIGITAL_DESIGN_KEYWORDS:
            if keyword in role:
                return "digital_design"

        for keyword in ANALOG_DESIGN_KEYWORDS:
            if keyword in role:
                return "analog_design"

        for keyword in EMBEDDED_SYSTEMS_KEYWORDS:
            if keyword in role:
                return "embedded_systems"

        for keyword in VLSI_KEYWORDS:
            if keyword in role:
                return "vlsi"

        # Product Management

        for keyword in PRODUCT_MANAGEMENT_KEYWORDS:
            if keyword in role:
                return "product_management"

        # Business domains

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

        # Software last (contains broader terms)

        for keyword in SOFTWARE_KEYWORDS:
            if keyword in role:
                return "software"

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
Digital_Design
Analog_Design
Embedded_Systems
VLSI
Product_Management

Interview Role:
{role}

Rules:
- Return ONLY one category.
- Use exactly one of the category names above.
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
            "digital_design",
            "analog_design",
            "embedded_systems",
            "vlsi",
            "product_management",
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
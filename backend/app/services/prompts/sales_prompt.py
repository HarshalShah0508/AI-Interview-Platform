"""
Sales interview prompt builder.
"""


def build_sales_prompt(
    role: str,
    difficulty: str,
    resume_text: str | None = None,
) -> str:
    """
    Builds the Gemini prompt for Sales interviews.

    Args:
        role: Candidate's selected role.
        difficulty: Easy / Medium / Hard.
        resume_text: Parsed resume text if available.

    Returns:
        Prompt string for Gemini.
    """

    if resume_text:

        return f"""
You are an expert Sales interviewer hiring for leading organizations such as Salesforce, Oracle, HubSpot, Microsoft, Amazon, Adobe, SAP and Cisco.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

Candidate Resume:
{resume_text}

Generate EXACTLY 10 interview questions.

Interview Structure

1. Resume-Based Questions (2)

- Ask exactly 2 questions based on the candidate's resume.
- Focus on sales experience, internships, achievements, targets, client handling, negotiations, leadership and measurable business impact.

2. Sales Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- Sales Funnel
- CRM
- Lead Generation

Medium
- Negotiation
- Prospecting
- Pipeline Management

Hard
- Enterprise Sales
- Sales Forecasting
- Strategic Selling
- Key Account Management
- Sales Metrics

Questions must strictly match the selected difficulty.

3. Customer Scenarios (2)

Generate exactly 2 customer-based scenario questions.

Difficulty Guidelines:

Easy
- Basic customer interactions

Medium
- Handling objections
- Closing deals
- Customer negotiations

Hard
- Enterprise customer scenarios
- Strategic negotiations
- Multi-stakeholder selling

4. Sales Strategy Questions (2)

Generate exactly 2 questions specific to the selected sales role.

Examples include:

- Business Development
- Account Executive
- Account Manager
- Customer Success
- Relationship Manager
- Inside Sales
- Enterprise Sales

Questions should assess practical sales thinking.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules

- Generate EXACTLY 10 questions.
- Match the selected role.
- Match the selected difficulty.
- Avoid duplicate concepts.
- Cover different sales competencies.
- Keep every question concise.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered questions.
"""

    return f"""
You are an expert Sales interviewer hiring for leading organizations such as Salesforce, Oracle, HubSpot, Microsoft, Amazon, Adobe, SAP and Cisco.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

The candidate has NOT provided a resume.

Generate EXACTLY 10 interview questions.

Interview Structure

1. Role-Specific Sales Questions (2)

Generate exactly 2 additional role-specific sales questions because no resume is available.

2. Sales Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- Sales Funnel
- CRM
- Lead Generation

Medium
- Negotiation
- Prospecting
- Pipeline Management

Hard
- Enterprise Sales
- Sales Forecasting
- Strategic Selling
- Key Account Management
- Sales Metrics

3. Customer Scenarios (2)

Generate exactly 2 customer scenario questions.

Difficulty must match the selected level.

4. Sales Strategy Questions (2)

Generate exactly 2 role-specific sales strategy questions.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules

- Generate EXACTLY 10 questions.
- Match the selected role.
- Match the selected difficulty.
- Avoid duplicate concepts.
- Keep questions concise.
- Do NOT provide answers.
- Return ONLY the numbered questions.
"""
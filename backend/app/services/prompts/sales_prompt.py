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
        difficulty: Easy /Medium / Hard.
        resume_text: Parsed resume text if available.

    Returns:
        Prompt string for Gemini.
    """

    if resume_text:

        return f"""
You are an expert Sales interviewer hiring for leading organizations such as Salesforce, Oracle, HubSpot, Microsoft, Amazon, Adobe, SAP and Cisco.

You are conducting a live interview, not creating an exam paper.

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

Interview Style Guidelines

- Ask every question in a natural, conversational and professional manner, similar to how an experienced interviewer would speak.
- Use simple, easy-to-understand English while preserving all important sales terminology and concepts.
- The difficulty should come from the business scenario or sales concept being tested, not from complicated wording.
- Do NOT simplify the business concepts. Only simplify the language used to ask the question.
- Encourage candidates to explain their reasoning, decision-making process and practical approach.
- Questions should feel like a genuine conversation during a real sales interview.

Avoid overly direct textbook-style questions such as:
- "Explain CRM."
- "Define Lead Generation."
- "What is Enterprise Sales?"

Instead, naturally introduce topics using a variety of conversational styles such as:
- "Let's talk about..."
- "Suppose you're meeting..."
- "Imagine you're handling..."
- "Can you walk me through..."
- "How would you approach..."
- "What would you do if..."
- "Have you experienced..."
- "Could you explain..."
- "Why do you think..."

Do NOT start every question with the same phrase.

Vary the wording naturally throughout the interview.

General Rules

- Generate EXACTLY 10 questions.
- Match the selected role.
- Match the selected difficulty.
- Avoid duplicate concepts.
- Cover different sales competencies.
- Keep every question concise while still being conversational.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered interview questions.

Do not include headings, introductions, markdown, bullet points or any text before or after the questions.
"""

    return f"""
You are an expert Sales interviewer hiring for leading organizations such as Salesforce, Oracle, HubSpot, Microsoft, Amazon, Adobe, SAP and Cisco.

You are conducting a live interview, not creating an exam paper.

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

Interview Style Guidelines

- Ask every question in a natural, conversational and professional manner, similar to how an experienced interviewer would speak.
- Use simple, easy-to-understand English while preserving all important sales terminology and concepts.
- The difficulty should come from the business scenario or sales concept being tested, not from complicated wording.
- Do NOT simplify the business concepts. Only simplify the language used to ask the question.
- Encourage candidates to explain their reasoning, decision-making process and practical approach.
- Questions should feel like a genuine conversation during a real sales interview.

Avoid overly direct textbook-style questions such as:
- "Explain CRM."
- "Define Lead Generation."
- "What is Enterprise Sales?"

Instead, naturally introduce topics using a variety of conversational styles such as:
- "Let's talk about..."
- "Suppose you're meeting..."
- "Imagine you're handling..."
- "Can you walk me through..."
- "How would you approach..."
- "What would you do if..."
- "Have you experienced..."
- "Could you explain..."
- "Why do you think..."

Do NOT start every question with the same phrase.

Vary the wording naturally throughout the interview.

General Rules

- Generate EXACTLY 10 questions.
- Match the selected role.
- Match the selected difficulty.
- Avoid duplicate concepts.
- Cover different sales competencies.
- Keep every question concise while still being conversational.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered interview questions.

Do not include headings, introductions, markdown, bullet points or any text before or after the questions.
"""
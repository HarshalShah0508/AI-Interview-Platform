"""
Marketing interview prompt builder.
"""


def build_marketing_prompt(
    role: str,
    difficulty: str,
    resume_text: str | None = None,
) -> str:
    """
    Builds the Gemini prompt for Marketing interviews.

    Args:
        role: Candidate's selected role.
        difficulty: Easy / Medium / Hard.
        resume_text: Parsed resume text if available.

    Returns:
        Prompt string for Gemini.
    """

    if resume_text:

        return f"""
You are an expert Marketing interviewer hiring for leading organizations such as Google, Amazon, Meta, Adobe, Unilever, Procter & Gamble, HubSpot and Salesforce.

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
- Focus on marketing campaigns, internships, projects, branding initiatives, leadership, certifications, measurable results and achievements.
- Use the resume extensively.

2. Marketing Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- Branding
- Marketing Mix (4Ps)
- SEO
- Consumer Behaviour
- Market Segmentation

Medium
- SEM
- Campaign Optimization
- Marketing Analytics
- Customer Journey
- Content Strategy

Hard
- Growth Marketing
- Attribution Models
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Marketing Automation
- Performance Marketing
- Omnichannel Strategy

Questions must strictly match the selected difficulty.

3. Campaign Case Studies (2)

Generate exactly 2 campaign-based case study questions.

Difficulty Guidelines:

Easy
- Basic campaign planning
- Product promotion
- Brand awareness

Medium
- Campaign optimization
- Budget allocation
- Performance improvement

Hard
- Multi-channel marketing strategy
- Growth experiments
- Data-driven campaign decisions
- Scaling marketing initiatives

4. Marketing Analytics Questions (2)

Generate exactly 2 role-specific marketing questions.

Examples include:

- Digital Marketing
- Brand Management
- Product Marketing
- Performance Marketing
- Growth Marketing
- SEO Specialist
- Content Marketing
- Marketing Analytics

Questions should evaluate practical marketing knowledge and decision-making.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules

- Generate EXACTLY 10 questions.
- Questions must match the selected role.
- Questions must match the selected difficulty.
- Avoid duplicate concepts.
- Cover different marketing competencies.
- Keep every question concise.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered questions.
"""

    return f"""
You are an expert Marketing interviewer hiring for leading organizations such as Google, Amazon, Meta, Adobe, Unilever, Procter & Gamble, HubSpot and Salesforce.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

The candidate has NOT provided a resume.

Generate EXACTLY 10 interview questions.

Interview Structure

1. Role-Specific Marketing Questions (2)

Generate exactly 2 additional role-specific marketing questions because no resume is available.

2. Marketing Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- Branding
- Marketing Mix (4Ps)
- SEO
- Consumer Behaviour
- Market Segmentation

Medium
- SEM
- Campaign Optimization
- Marketing Analytics
- Customer Journey
- Content Strategy

Hard
- Growth Marketing
- Attribution Models
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Marketing Automation
- Performance Marketing
- Omnichannel Strategy

3. Campaign Case Studies (2)

Generate exactly 2 campaign case-study questions.

Difficulty must match the selected level.

4. Marketing Analytics Questions (2)

Generate exactly 2 role-specific marketing analytics questions.

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
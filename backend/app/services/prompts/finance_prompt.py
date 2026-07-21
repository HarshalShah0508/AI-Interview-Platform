"""
Finance interview prompt builder.
"""


def build_finance_prompt(
    role: str,
    difficulty: str,
    resume_text: str | None = None,
) -> str:
    """
    Builds the Gemini prompt for Finance interviews.

    Args:
        role: Candidate's selected role.
        difficulty: Easy / Medium / Hard.
        resume_text: Parsed resume text if available.

    Returns:
        Prompt string for Gemini.
    """

    if resume_text:

        return f"""
You are an expert Finance interviewer hiring for leading organizations such as Goldman Sachs, JPMorgan Chase, Morgan Stanley, BlackRock, KPMG, Deloitte, EY and PwC.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

Candidate Resume:
{resume_text}

Generate EXACTLY 10 interview questions.

Interview Structure

1. Resume-Based Questions (2)

- Ask exactly 2 questions from the candidate's resume.
- Focus on internships, financial projects, certifications, investment experience, accounting knowledge, leadership and achievements.

2. Finance Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- Accounting
- Financial Statements
- Ratio Analysis

Medium
- DCF
- Valuation
- CAPM
- NPV
- IRR

Hard
- Derivatives
- Portfolio Theory
- Financial Modeling
- Advanced Valuation
- Risk Management

Questions must match the selected difficulty.

3. Finance Case Studies (2)

Generate exactly 2 real interview case-study questions.

Difficulty Guidelines:

Easy
- Simple business situations

Medium
- Financial analysis and investment decisions

Hard
- Multi-step valuation, risk analysis and strategic financial decisions

4. Role-Specific Technical Questions (2)

Generate exactly 2 questions specifically related to the selected role.

Examples include:

Investment Banking
Equity Research
Corporate Finance
Risk Management
Financial Analyst
Treasury
Asset Management
Private Equity
Venture Capital

Match the difficulty.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules

- Generate EXACTLY 10 questions.
- Questions must match the selected role.
- Questions must match the selected difficulty.
- Avoid duplicate concepts.
- Keep every question concise.
- Do NOT provide answers.
- Return ONLY the numbered questions.
"""

    return f"""
You are an expert Finance interviewer hiring for leading organizations such as Goldman Sachs, JPMorgan Chase, Morgan Stanley, BlackRock, KPMG, Deloitte, EY and PwC.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

The candidate has NOT provided a resume.

Generate EXACTLY 10 interview questions.

Interview Structure

1. Role-Specific Questions (2)

Generate exactly 2 additional finance role-specific questions because no resume is available.

2. Finance Fundamentals (3)

Difficulty Guidelines:

Easy
- Accounting
- Financial Statements
- Ratio Analysis

Medium
- DCF
- Valuation
- CAPM
- NPV
- IRR

Hard
- Derivatives
- Portfolio Theory
- Financial Modeling
- Advanced Valuation
- Risk Management

Generate exactly 3 questions.

3. Finance Case Studies (2)

Generate exactly 2 case-study questions.

Difficulty must match the selected level.

4. Role-Specific Technical Questions (2)

Generate exactly 2 questions related to the selected finance role.

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
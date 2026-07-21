"""
Consulting interview prompt builder.
"""


def build_consulting_prompt(
    role: str,
    difficulty: str,
    resume_text: str | None = None,
) -> str:
    """
    Builds the Gemini prompt for Consulting interviews.

    Args:
        role: Candidate's selected role.
        difficulty: Easy /Medium / Hard.
        resume_text: Parsed resume text if available.

    Returns:
        Prompt string for Gemini.
    """

    if resume_text:

        return f"""
You are an expert Management Consulting interviewer hiring for leading consulting firms such as McKinsey & Company, Boston Consulting Group (BCG), Bain & Company, Accenture Strategy, Deloitte Consulting, EY-Parthenon, Kearney and Oliver Wyman.

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
- Focus on internships, leadership experiences, business projects, achievements, problem-solving experience, impact created and decision making.

2. Consulting Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- SWOT Analysis
- Porter's Five Forces
- PESTLE Analysis

Medium
- Market Entry Strategy
- Profitability Framework
- Growth Strategy

Hard
- M&A Strategy
- Corporate Transformation
- Organizational Strategy
- Competitive Strategy
- Business Transformation

Questions must match the selected difficulty.

3. Business Case Studies (2)

Generate exactly 2 consulting case interview questions.

Difficulty Guidelines:

Easy
- Simple business scenarios

Medium
- Structured business case interviews

Hard
- Multi-step strategic consulting cases involving analysis and recommendations

4. Business Analysis Questions (2)

Generate exactly 2 business analysis questions related to the selected consulting role.

Examples include:

- Strategy Consulting
- Operations Consulting
- Business Consulting
- Advisory
- Management Consulting
- Digital Consulting

Match the selected difficulty.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules

- Generate EXACTLY 10 questions.
- Questions must match the selected role.
- Questions must match the selected difficulty.
- Avoid duplicate concepts.
- Cover different business domains.
- Keep every question concise.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered questions.
"""

    return f"""
You are an expert Management Consulting interviewer hiring for leading consulting firms such as McKinsey & Company, Boston Consulting Group (BCG), Bain & Company, Accenture Strategy, Deloitte Consulting, EY-Parthenon, Kearney and Oliver Wyman.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

The candidate has NOT provided a resume.

Generate EXACTLY 10 interview questions.

Interview Structure

1. Role-Specific Consulting Questions (2)

Generate exactly 2 consulting role-specific questions since no resume is available.

2. Consulting Fundamentals (3)

Generate exactly 3 questions.

Difficulty Guidelines:

Easy
- SWOT Analysis
- Porter's Five Forces
- PESTLE Analysis

Medium
- Market Entry Strategy
- Profitability Framework
- Growth Strategy

Hard
- M&A Strategy
- Corporate Transformation
- Organizational Strategy
- Competitive Strategy
- Business Transformation

3. Business Case Studies (2)

Generate exactly 2 consulting case interview questions.

Difficulty must match the selected level.

4. Business Analysis Questions (2)

Generate exactly 2 consulting role-specific analytical questions.

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
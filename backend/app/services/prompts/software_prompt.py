"""
Software interview prompt builder.

This module contains the original software interview prompt that was
previously embedded inside ai_service.py.

IMPORTANT:
- Do NOT modify the interview structure.
- Do NOT modify the question distribution.
- Do NOT modify the difficulty behavior.
- Do NOT modify the resume/no-resume behavior.

This prompt has only been moved into its own module to support
clean routing for multiple interview categories.
"""


def build_software_prompt(
    role: str,
    difficulty: str,
    resume_text: str | None = None,
) -> str:
    """
    Build the Gemini prompt for Software Engineering interviews.

    Args:
        role: Candidate's selected role.
        difficulty: Easy / Medium / Hard.
        resume_text: Parsed resume text if available.

    Returns:
        Complete prompt string to send to Gemini.
    """

    if resume_text:

        return f"""
You are an expert Software Engineering interviewer at top product-based companies like Google, Amazon, Microsoft, Meta, Apple, Netflix and Uber.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

Candidate Resume:
{resume_text}

Generate EXACTLY 10 interview questions.

Interview Structure:

1. Resume-Based Questions (2)
- Ask exactly 2 questions based on the candidate's resume.
- Focus on projects, internships, technologies used, architecture, implementation choices, optimizations, challenges faced and achievements.
- Use the resume extensively.

2. Core Computer Science Fundamentals (3)
Generate exactly 3 questions.

Focus primarily on:
- Operating Systems
- Database Management Systems (DBMS)
- Object-Oriented Programming (OOP)

Use Computer Networks only if it is relevant to the selected role.

Adjust the complexity according to the interview difficulty:
- Easy → basic concepts and definitions
- Medium → application-based interview questions
- Hard → advanced concepts, trade-offs and real interview scenarios

3. Coding / DSA (2)
Generate exactly 2 coding questions.

Requirements:
- Famous interview problems.
- Appropriate for the selected difficulty.
- Easy → LeetCode Easy
- Medium → LeetCode Medium
- Hard → LeetCode Hard
- Do NOT provide solutions.
- Only provide the problem statements.

4. System Design Concepts (2)
Generate exactly 2 conceptual System Design questions.

DO NOT ask candidates to design systems such as:
- Design Twitter
- Design WhatsApp
- Design YouTube
- Design Uber

Instead ask conceptual interview questions on topics such as:
- Caching
- Load Balancing
- Database Indexing
- Replication
- Sharding
- Horizontal vs Vertical Scaling
- CAP Theorem
- Message Queues
- API Gateway
- Microservices
- CDN
- Rate Limiting
- Consistency
- Fault Tolerance

Increase the conceptual depth according to the selected difficulty.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules:
- Generate EXACTLY 10 questions.
- Questions must match the selected role.
- Questions must match the selected difficulty.
- Avoid duplicate concepts.
- Cover a variety of topics.
- Questions should resemble real Software Engineering interviews.
- Keep every question concise.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered questions.
"""

    return f"""
You are an expert Software Engineering interviewer at top product-based companies like Google, Amazon, Microsoft, Meta, Apple, Netflix and Uber.

Candidate Role:
{role}

Interview Difficulty:
{difficulty}

The candidate has NOT provided a resume.

Generate EXACTLY 10 interview questions.

Interview Structure:

1. Role-Specific Technical Questions (2)

Since there is no resume, generate 2 additional role-specific technical questions.

2. Core Computer Science Fundamentals (3)

Focus primarily on:
- Operating Systems
- Database Management Systems (DBMS)
- Object-Oriented Programming (OOP)

Use Computer Networks only if it is relevant to the selected role.

Adjust the complexity according to the selected difficulty:
- Easy → basic concepts
- Medium → application-based interview questions
- Hard → advanced concepts and scenarios

3. Coding / DSA (2)

Generate exactly 2 coding questions.

Requirements:
- Famous interview problems.
- Easy → LeetCode Easy
- Medium → LeetCode Medium
- Hard → LeetCode Hard
- Do NOT provide solutions.

4. System Design Concepts (2)

Generate exactly 2 conceptual System Design questions.

DO NOT ask candidates to design complete systems.

Instead ask conceptual interview questions about:
- Caching
- Load Balancing
- Database Indexing
- Replication
- Sharding
- Horizontal vs Vertical Scaling
- CAP Theorem
- Message Queues
- API Gateway
- Microservices
- CDN
- Rate Limiting
- Consistency
- Fault Tolerance

Increase the conceptual depth according to the selected difficulty.

5. Behavioral Question (1)

Generate exactly 1 behavioral interview question.

General Rules:
- Generate EXACTLY 10 questions.
- Match the selected role.
- Match the selected difficulty.
- Avoid duplicate concepts.
- Cover different topics.
- Keep questions concise.
- Do NOT provide answers, hints or explanations.

Return ONLY the numbered questions.
"""
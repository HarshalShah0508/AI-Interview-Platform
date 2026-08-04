"""
Evaluation prompt builder.

This module contains the prompt used to evaluate a candidate's interview
answer. The prompt is intentionally separated from AIService so that all
prompt engineering lives under the prompts package.

IMPORTANT:
- Do NOT modify the JSON response schema without updating the parser.
- Do NOT modify the score range unless the parser is updated.
"""


def build_evaluation_prompt(
    question_text: str,
    user_answer: str,
) -> str:
    """
    Build the Gemini prompt for evaluating interview answers.

    Args:
        question_text: Interview question.
        user_answer: Candidate's combined answer.

    Returns:
        Complete evaluation prompt.
    """

    return f"""
You are an expert technical interviewer evaluating a candidate's interview answer.

Your task is to evaluate the candidate's answer for the given interview question.

Evaluate the answer on these 3 dimensions:

1. Technical Correctness
   - Are the concepts factually correct?
   - Is the explanation technically sound?
   - Are important technical terms used properly?

2. Completeness
   - Does the answer fully address the question?
   - Are important points missing?
   - Is the explanation sufficiently developed for an interview setting?

3. Communication Clarity
   - Is the answer clear and understandable?
   - Is it logically structured?
   - Does it communicate the idea well in a professional interview context?

Scoring Rules:
- Return a single overall score from 1 to 10.
- 1 to 3 = largely incorrect, extremely incomplete, or very unclear
- 4 to 6 = partially correct but missing important points or lacking clarity
- 7 to 8 = mostly correct, reasonably complete, and fairly clear, with some room for improvement
- 9 to 10 = highly correct, complete, clear, and interview-ready

Return ONLY valid JSON.
Do not include markdown.
Do not include code fences.
Do not include explanations outside JSON.
Do not include any extra text before or after the JSON.

The JSON must follow exactly this structure:
{{
  "score": 8,
  "feedback": "Overall evaluation summary here",
  "strengths": [
    "Strength 1",
    "Strength 2"
  ],
  "improvements": [
    "Improvement 1",
    "Improvement 2"
  ]
}}

Rules for the JSON fields:
- "score" must be an integer from 1 to 10
- "feedback" must be a concise but useful overall evaluation summary
- "strengths" must be a JSON array of 2 to 4 short bullet-style strings
- "improvements" must be a JSON array of 2 to 4 short bullet-style strings
- All values must be based only on the question and answer provided below

Interview Question:
{question_text}

Candidate Answer:
{user_answer}
""".strip()

def build_follow_up_prompt(
    original_question: str,
    candidate_answer: str,
    evaluation: dict,
    follow_up_depth: int,
) -> str:
    """
    Builds a prompt for generating a follow-up interview question.

    Args:
        original_question: The main interview question.
        candidate_answer: The candidate's answer.
        evaluation: Parsed evaluation dictionary returned by Gemini.
        follow_up_depth: Current follow-up depth (1 or 2).

    Returns:
        Prompt string for Gemini.
    """

    next_depth = follow_up_depth + 1

    return f"""
You are an expert interviewer conducting a professional interview.

The candidate answered the following interview question well enough that you want
to explore the SAME topic in greater depth.

Generate EXACTLY ONE follow-up interview question.

Original Question:
{original_question}

Candidate Answer:
{candidate_answer}

Evaluation Score:
{evaluation["score"]}/10

Evaluation Summary:
{evaluation["feedback"]}

Strengths:
{chr(10).join("- " + s for s in evaluation["strengths"])}

Areas for Improvement:
{chr(10).join("- " + i for i in evaluation["improvements"])}

Current Follow-up Depth:
{follow_up_depth}

Next Follow-up Depth:
{next_depth}

Requirements

- Stay on EXACTLY the same topic.
- Do NOT introduce a completely new topic.
- The follow-up should naturally continue the discussion.
- Make the question slightly more challenging than the previous one.
- Encourage reasoning, practical thinking and trade-offs.
- Do NOT repeat the original question.
- Do NOT ask a definition that has already been answered.
- Assume the candidate has demonstrated a reasonable understanding of the topic.

Interview Style Guidelines

- Ask the follow-up question in a natural, conversational and professional manner.
- Use simple, easy-to-understand English while preserving all important technical or domain terminology.
- The difficulty should come from the concepts being tested, not from complicated wording.
- The follow-up should feel like a natural continuation of the discussion.
- Encourage the candidate to explain reasoning, implementation decisions, trade-offs or design choices.

Avoid textbook-style questions such as:

- Explain...
- Define...
- What is...

Instead naturally continue the discussion using phrases such as:

- Let's go a little deeper into that...
- You mentioned...
- Could you expand on...
- Suppose we change the situation slightly...
- Imagine you're working on...
- Can you walk me through...
- How would your approach change if...
- Why do you think...
- What trade-offs would you consider...

Do NOT start every follow-up with the same phrase.

Vary the wording naturally.

Difficulty Progression

If Next Follow-up Depth is 1:
- Ask about application.
- Ask for an example.
- Ask about practical implementation.

If Next Follow-up Depth is 2:
- Ask about trade-offs.
- Ask about edge cases.
- Ask about optimization.
- Ask about real-world scenarios.
- Ask about architecture or design decisions.

General Rules

- Generate EXACTLY ONE follow-up question.
- Return ONLY the question.
- Do NOT number the question.
- Do NOT provide answers.
- Do NOT provide explanations.
- Do NOT include markdown.
""".strip()
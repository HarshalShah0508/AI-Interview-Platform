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
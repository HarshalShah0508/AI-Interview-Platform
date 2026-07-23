import json

from app.services.role_classifier import RoleClassifier
from app.services.api_key_manager import APIKeyManager
from app.services.prompts.software_prompt import build_software_prompt
from app.services.prompts.finance_prompt import build_finance_prompt
from app.services.prompts.consulting_prompt import build_consulting_prompt
from app.services.prompts.sales_prompt import build_sales_prompt
from app.services.prompts.marketing_prompt import build_marketing_prompt


class AIService:

    def __init__(self):

        self.key_manager = APIKeyManager()

        self.role_classifier = RoleClassifier()

    def generate_questions(
        self,
        resume_text: str | None,
        role: str,
        difficulty: str,
    ):

        category = self.role_classifier.classify_role(
            role=role,
            model=self.key_manager.get_model(),
        )

        if category == "software":

            prompt = build_software_prompt(
                role=role,
                difficulty=difficulty,
                resume_text=resume_text,
            )

        elif category == "finance":

            prompt = build_finance_prompt(
                role=role,
                difficulty=difficulty,
                resume_text=resume_text,
            )

        elif category == "consulting":

            prompt = build_consulting_prompt(
                role=role,
                difficulty=difficulty,
                resume_text=resume_text,
            )

        elif category == "sales":

            prompt = build_sales_prompt(
                role=role,
                difficulty=difficulty,
                resume_text=resume_text,
            )

        elif category == "marketing":

            prompt = build_marketing_prompt(
                role=role,
                difficulty=difficulty,
                resume_text=resume_text,
            )

        else:

            prompt = build_software_prompt(
                role=role,
                difficulty=difficulty,
                resume_text=resume_text,
            )

        print("\n========== SELECTED ROLE ==========")
        print(role)

        print("\n========== INTERVIEW CATEGORY ==========")
        print(category)

        response = self.key_manager.generate_content(
            prompt
        )

        print("\n===== GEMINI QUESTION RESPONSE =====\n")
        print(response)

        return response.text
    def build_combined_answer(
        self,
        voice_text: str | None,
        typed_text: str | None,
        code: str | None
    ) -> str:

        sections = []

        if voice_text and voice_text.strip():
            sections.append(
                f"Explanation:\n{voice_text.strip()}"
            )

        if typed_text and typed_text.strip():
            sections.append(
                f"Additional Notes:\n{typed_text.strip()}"
            )

        if code and code.strip():
            sections.append(
                f"Code:\n{code.strip()}"
            )

        if not sections:
            raise ValueError(
                "At least one of voice_text, typed_text or code must be provided."
            )

        return "\n\n".join(sections)

    def build_evaluation_prompt(
        self,
        question_text: str,
        user_answer: str
    ) -> str:

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

    def parse_evaluation_response(
        self,
        response_text: str
    ) -> dict:

        try:
            parsed_response = json.loads(
                response_text.strip()
            )
        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned invalid JSON for answer evaluation."
            )

        required_keys = [
            "score",
            "feedback",
            "strengths",
            "improvements"
        ]

        for key in required_keys:
            if key not in parsed_response:
                raise ValueError(
                    f"Missing key '{key}' in Gemini evaluation response."
                )

        score = parsed_response["score"]
        feedback = parsed_response["feedback"]
        strengths = parsed_response["strengths"]
        improvements = parsed_response["improvements"]

        if not isinstance(score, int):
            raise ValueError("Gemini evaluation score must be an integer.")

        if score < 1 or score > 10:
            raise ValueError("Gemini evaluation score must be between 1 and 10.")

        if not isinstance(feedback, str):
            raise ValueError("Gemini evaluation feedback must be a string.")

        if not isinstance(strengths, list):
            raise ValueError("Gemini evaluation strengths must be a list.")

        if not isinstance(improvements, list):
            raise ValueError("Gemini evaluation improvements must be a list.")

        if not all(isinstance(item, str) for item in strengths):
            raise ValueError("All strengths must be strings.")

        if not all(isinstance(item, str) for item in improvements):
            raise ValueError("All improvements must be strings.")

        return {
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "improvements": improvements
        }

    def evaluate_answer(
        self,
        question_text: str,
        user_answer: str
    ) -> dict:

        prompt = self.build_evaluation_prompt(
            question_text=question_text,
            user_answer=user_answer
        )

        response = self.key_manager.generate_content(
            prompt
        )

        print("\n===== GEMINI ANSWER EVALUATION RESPONSE =====\n")
        print(response)

        return self.parse_evaluation_response(
            response.text
        )
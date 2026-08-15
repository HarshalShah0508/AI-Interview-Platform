import json
from io import BytesIO

from fastapi import UploadFile
from google.genai import types
from pypdf import PdfReader
from app.core.config import GEMINI_MODEL

from app.services.api_key_manager import (
    api_key_manager,
)
from app.schemas.resume_analysis import JDProfile


class JobDescriptionParser:

    async def extract_pdf_text(
        self,
        file: UploadFile,
    ) -> str:

        content = await file.read()

        reader = PdfReader(
            BytesIO(content)
        )

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text and text.strip():
                pages.append(
                    text.strip()
                )

        extracted_text = "\n\n".join(
            pages
        ).strip()

        if not extracted_text:
            raise ValueError(
                "Could not extract text from the PDF."
            )

        return extracted_text

    async def extract_image_text(
        self,
        file: UploadFile,
    ) -> str:

        image_bytes = await file.read()

        mime_type = file.content_type

        allowed_types = {
            "image/png",
            "image/jpeg",
            "image/webp",
            "image/heic",
            "image/heif",
        }

        if mime_type not in allowed_types:
            raise ValueError(
                "Unsupported image format."
            )

        prompt = """
You are extracting a Job Description from an image.

Read the image carefully.

Extract the COMPLETE visible job description.

Preserve:
- Job title
- Responsibilities
- Required qualifications
- Preferred qualifications
- Technical skills
- Soft skills
- Experience requirements
- Education requirements
- Certifications
- Years of experience
- Named technologies
- Frameworks
- Programming languages
- Tools
- Cloud platforms
- Important numbers

Do NOT summarize.

Do NOT invent missing information.

Do NOT add information that is not visible.

Return only the extracted job description text.
"""

        response = api_key_manager.generate_content(
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            prompt,
            ],
            purpose="jd_image_ocr",
        )

        text = (
            response.text or ""
        ).strip()

        if not text:
            raise ValueError(
                "Could not extract text from the image."
            )

        return text

    async def extract_job_description(
        self,
        text: str | None = None,
        file: UploadFile | None = None,
    ) -> str:

        if text and text.strip():
            return text.strip()

        if not file:
            raise ValueError(
                "Provide either JD text or a JD file."
            )

        content_type = (
            file.content_type or ""
        ).lower()

        if content_type == "application/pdf":
            return await self.extract_pdf_text(
                file
            )

        if content_type.startswith("image/"):
            return await self.extract_image_text(
                file
            )

        raise ValueError(
            "Unsupported JD format. "
            "Supported formats: PDF, PNG, JPEG, WEBP."
        )

    def structure_job_description(
        self,
        job_description: str,
    ) -> JDProfile:

        prompt = f"""
You are the Job Description Intelligence Engine
for Hot Seat.

Analyze the following job description.

JOB DESCRIPTION
================
{job_description}
================

Your job is to convert it into a structured representation.

STRICT RULES:

1. Extract ONLY information supported by the JD.

2. NEVER invent requirements.

3. Separate:
   - technical skills
   - responsibilities
   - soft skills
   - experience
   - education
   - certifications
   - domain knowledge
   - tools

4. Determine whether each requirement is:
   - required
   - preferred
   - nice_to_have
   - unclear

5. Assign importance from 1 to 10.

10:
Explicitly required or central to the role.

8-9:
Very important requirement.

6-7:
Important requirement.

4-5:
Preferred requirement.

1-3:
Minor / nice-to-have requirement.

6. Extract important keywords.

Do NOT include generic words such as:
candidate
company
team
work
skills
experience

unless they are part of a meaningful requirement.

7. Normalize obvious aliases.

Valid examples:

Postgres → PostgreSQL
RESTful API → REST API
JS → JavaScript

8. DO NOT treat different technologies as aliases.

For example:

AWS != Azure
AWS != GCP
Docker != Kubernetes
React != Angular
Python != Java

9. Preserve evidence from the JD supporting
each important requirement.

10. Do not infer a requirement merely because
it is common for the role.

11. If the JD is ambiguous, mark the requirement
as "unclear".

12. The final representation must be useful for
matching the JD against a candidate's resume.

13. COMPOUND REQUIREMENTS:

Some requirement names conjoin two or more distinct
concepts, usually joined by "and", "&", "/", or a comma.

Examples of compound requirement names:

"Frontend Technologies & Web Services"
"Code Review and Production Safety"
"Collaborative Coding Experience"

For each requirement whose name bundles multiple
distinct concepts together, populate "components"
with short, atomic concept names — one per distinct
concept, using plain lowercase phrases.

Examples:

"Frontend Technologies & Web Services"
components: ["frontend technologies", "web services"]

"Code Review and Production Safety"
components: ["code review", "production safety"]

"Collaborative Coding Experience"
components: ["collaborative coding experience"]
(a single concept — do NOT invent a split that
is not actually present in the requirement name)

If a requirement already names exactly one concept,
leave "components" empty. Do NOT split a single
concept into unrelated fragments merely to populate
this field.

Return ONLY structured data matching the schema.
"""

        response = api_key_manager.generate_content(
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JDProfile,
            ),
            purpose="jd_structuring",
        )

        raw_response = (
            response.text or ""
        ).strip()

        if not raw_response:
            raise ValueError(
                "Gemini returned an empty JD analysis."
            )

        try:

            parsed = json.loads(
                raw_response
            )

            return JDProfile.model_validate(
                parsed
            )

        except Exception as exc:

            raise ValueError(
                "Gemini returned an invalid "
                "structured JD response."
            ) from exc
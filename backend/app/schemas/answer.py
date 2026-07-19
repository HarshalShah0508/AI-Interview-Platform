from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel


class AnswerCreate(BaseModel):
    question_id: int

    voice_text: Optional[str] = None
    typed_text: Optional[str] = None
    code: Optional[str] = None


class AnswerResponse(BaseModel):
    answer_id: int
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]


class AnswerDetail(BaseModel):
    id: int
    question_id: int

    voice_text: Optional[str]
    typed_text: Optional[str]
    code: Optional[str]

    combined_answer: str

    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]

    created_at: datetime

    class Config:
        from_attributes = True


class SessionResultsResponse(BaseModel):
    session_id: int
    average_score: float
    questions_attempted: int
    strong_topics: List[str]
    weak_topics: List[str]
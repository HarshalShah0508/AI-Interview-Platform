from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.answer import Answer
from app.models.question import Question
from app.models.interview_session import InterviewSession
from app.models.user import User
from app.schemas.answer import (
    AnswerCreate,
    AnswerResponse,
    AnswerDetail,
    SessionResultsResponse,
)
from app.services.ai_service import AIService
from app.api.auth import get_current_user


router = APIRouter(
    prefix="/answer",
    tags=["Answer Evaluation"]
)


@router.post(
    "",
    response_model=AnswerResponse
)
def submit_answer(
    payload: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = (
        db.query(Question)
        .filter(Question.id == payload.question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )

    if question.session.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to answer this question."
        )

    existing_answer = (
        db.query(Answer)
        .filter(Answer.question_id == question.id)
        .first()
    )

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="This question has already been answered."
        )

    ai_service = AIService()

    try:
        combined_answer = ai_service.build_combined_answer(
            voice_text=payload.voice_text,
            typed_text=payload.typed_text,
            code=payload.code
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    evaluation = ai_service.evaluate_answer(
        question_text=question.question_text,
        user_answer=combined_answer
    )

    answer = Answer(
        question_id=question.id,

        voice_text=payload.voice_text,
        typed_text=payload.typed_text,
        code=payload.code,
        combined_answer=combined_answer,

        score=evaluation["score"],
        feedback=evaluation["feedback"],
        strengths=evaluation["strengths"],
        improvements=evaluation["improvements"],
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return AnswerResponse(
        answer_id=answer.id,
        score=answer.score,
        feedback=answer.feedback,
        strengths=answer.strengths,
        improvements=answer.improvements,
    )


@router.get(
    "/{answer_id}",
    response_model=AnswerDetail
)
def get_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    answer = (
        db.query(Answer)
        .filter(Answer.id == answer_id)
        .first()
    )

    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Answer not found."
        )

    if answer.question.session.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this answer."
        )

    return answer


@router.get(
    "/session/{session_id}/results",
    response_model=SessionResultsResponse
)
def get_session_results(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = (
        db.query(InterviewSession)
        .filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    questions = (
        db.query(Question)
        .filter(Question.session_id == session.id)
        .all()
    )

    answered_questions = [
        question
        for question in questions
        if question.answer
    ]

    if not answered_questions:
        return SessionResultsResponse(
            session_id=session.id,
            average_score=0.0,
            questions_attempted=0,
            strong_topics=[],
            weak_topics=[],
        )

    total_score = 0
    strong_topics = []
    weak_topics = []

    for question in answered_questions:
        answer = question.answer

        total_score += answer.score

        topic = question.question_text

        if len(topic) > 80:
            topic = topic[:80] + "..."

        if answer.score >= 8:
            strong_topics.append(topic)
        elif answer.score <= 5:
            weak_topics.append(topic)

    average_score = total_score / len(answered_questions)

    return SessionResultsResponse(
        session_id=session.id,
        average_score=round(average_score, 2),
        questions_attempted=len(answered_questions),
        strong_topics=strong_topics,
        weak_topics=weak_topics,
    )
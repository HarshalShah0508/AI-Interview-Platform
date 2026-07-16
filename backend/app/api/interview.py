from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.api.auth import get_current_user

from app.models.user import User
from app.models.resume import Resume
from app.models.interview_session import InterviewSession
from app.models.question import Question

from app.schemas.interview import GenerateQuestionsRequest
from app.schemas.interview import InterviewDetailResponse
from app.schemas.interview import InterviewHistoryItem

from app.services.ai_service import AIService


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


@router.post("/generate-questions")
def generate_questions(
    request: GenerateQuestionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    ) 

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    ai_service = AIService()

    questions = ai_service.generate_questions(
        resume_text=resume.extracted_text,
        role=request.role,
        difficulty=request.difficulty
    )

    question_list = []

    for line in questions.split("\n"):

        line = line.strip()

        if (
            line.startswith("1.")
            or line.startswith("2.")
            or line.startswith("3.")
            or line.startswith("4.")
            or line.startswith("5.")
            or line.startswith("6.")
            or line.startswith("7.")
            or line.startswith("8.")
            or line.startswith("9.")
            or line.startswith("10.")
        ):
            question_list.append(line)

    print("QUESTIONS FOUND:")
    print(len(question_list))

    session = InterviewSession(
        user_id=current_user.id,
        role=request.role,
        difficulty=request.difficulty
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    for question_text in question_list:
        question = Question(
            session_id=session.id,
            question_text=question_text
        )
        db.add(question)

    db.commit()

    return {
        "session_id": session.id,
        "role": session.role,
        "difficulty": session.difficulty,
        "questions_saved": len(question_list),
        "questions": questions
    }


@router.get(
    "/history",
    response_model=list[InterviewHistoryItem]
)
def get_interview_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    sessions = db.query(
        InterviewSession
    ).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(
        InterviewSession.created_at.desc()
    ).all()

    history = []

    for session in sessions:
        history.append(
            {
                "session_id": session.id,
                "role": session.role,
                "difficulty": session.difficulty,
                "created_at": session.created_at
            }
        )

    return history


@router.get(
    "/{session_id}",
    response_model=InterviewDetailResponse
)
def get_interview(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = (
        db.query(InterviewSession)
        .filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    questions = (
        db.query(Question)
        .filter(Question.session_id == session.id)
        .all()
    )

    question_list = []

    for question in questions:

        if question.answer:
            question_list.append(
                {
                    "id": question.id,
                    "question_text": question.question_text,
                    "answered": True,
                    "score": question.answer.score,
                    "feedback": question.answer.feedback,
                    "strengths": question.answer.strengths,
                    "improvements": question.answer.improvements,
                }
            )

        else:
            question_list.append(
                {
                    "id": question.id,
                    "question_text": question.question_text,
                    "answered": False,
                    "score": None,
                    "feedback": None,
                    "strengths": [],
                    "improvements": [],
                }
            )

    return {
        "session_id": session.id,
        "role": session.role,
        "difficulty": session.difficulty,
        "created_at": session.created_at,
        "questions": question_list,
    }
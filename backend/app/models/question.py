from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database.database import Base


class Question(Base):

    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False
    )

    question_text = Column(
        Text,
        nullable=False
    )

    session = relationship(
        "InterviewSession",
        back_populates="questions"
    )

    answer = relationship(
        "Answer",
        back_populates="question",
        uselist=False
    )
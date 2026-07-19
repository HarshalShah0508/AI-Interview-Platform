from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.interview import router as interview_router
from app.api.answer import router as answer_router
from app.api.dashboard import router as dashboard_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(answer_router)
app.include_router(dashboard_router)
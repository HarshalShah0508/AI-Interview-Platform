from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.interview import router as interview_router
from app.api.answer import router as answer_router
from app.api.dashboard import router as dashboard_router
from app.api import code
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",          # Docker frontend
        "http://localhost:5173",          # Vite frontend
        "http://127.0.0.1:5173",          # Vite frontend (127.0.0.1)
        "https://hotseatai.vercel.app",   # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(answer_router)
app.include_router(dashboard_router)
app.include_router(code.router)
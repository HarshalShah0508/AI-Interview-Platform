import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180)
)

UPLOAD_DIR = BASE_DIR / "uploads"

RESUME_DIR = UPLOAD_DIR / "resumes"

RESUME_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -----------------------------
# Gemini Configuration
# -----------------------------

GEMINI_API_KEYS = [
    key.strip()
    for key in os.getenv(
        "GEMINI_API_KEYS",
        ""
    ).split(",")
    if key.strip()
]

if not GEMINI_API_KEYS:
    raise ValueError(
        "At least one Gemini API key must be provided in GEMINI_API_KEYS."
    )
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

raw_keys = os.getenv("GEMINI_API_KEYS")

print("DEBUG GEMINI_API_KEYS:", repr(raw_keys))

GEMINI_API_KEYS = [
    key.strip()
    for key in (raw_keys or "").split(",")
    if key.strip()
]

if not GEMINI_API_KEYS:
    raise ValueError(
        f"At least one Gemini API key must be provided in GEMINI_API_KEYS. Received: {repr(raw_keys)}"
    )
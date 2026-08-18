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
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not GOOGLE_CLIENT_ID:
    raise ValueError(
        "GOOGLE_CLIENT_ID must be set in the environment."
    )

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

UPLOAD_DIR = BASE_DIR / "uploads"

RESUME_DIR = UPLOAD_DIR / "resumes"

RESUME_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -----------------------------
# Gemini Configuration
# -----------------------------

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash",
)

raw_keys = os.getenv("GEMINI_API_KEYS")

GEMINI_API_KEYS = [
    key.strip()
    for key in (raw_keys or "").split(",")
    if key.strip()
]

if not GEMINI_API_KEYS:
    raise ValueError(
        f"At least one Gemini API key must be provided in GEMINI_API_KEYS. Received: {repr(raw_keys)}"
    )

FOLLOW_UP_SCORE_THRESHOLD = 5

GEMINI_SEMANTIC_VERIFICATION_BATCH_SIZE = int(
    os.getenv("GEMINI_SEMANTIC_VERIFICATION_BATCH_SIZE", 12)
)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

SENDER_NAME = os.getenv(
    "SENDER_NAME",
    "Hot Seat"
)

SENDER_EMAIL = os.getenv(
    "SENDER_EMAIL"
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
)
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Project Paths
BASE_DIR = Path.cwd()

UPLOAD_DIR = BASE_DIR / "uploads"

RESUME_DIR = UPLOAD_DIR / "resumes"

RESUME_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Security Settings
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

# AI Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
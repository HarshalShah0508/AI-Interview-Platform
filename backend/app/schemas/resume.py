from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.resume import Resume
from app.services.pdf_parser import extract_text_from_pdf

class ResumeResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    created_at: datetime
    original_filename: str
    model_config = {
        "from_attributes": True
    }
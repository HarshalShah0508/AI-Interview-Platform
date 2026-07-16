from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from app.database.database import get_db
from app.core.config import RESUME_DIR
from sqlalchemy.orm import Session
from app.models.user import User
from app.api.auth import get_current_user
from app.models.resume import Resume
from app.services.pdf_parser import extract_text_from_pdf
from app.schemas.resume import ResumeResponse
router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    extension = Path(file.filename).suffix

    unique_filename = f"{uuid4()}{extension}"

    file_path = RESUME_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    extracted_text = extract_text_from_pdf(
    str(file_path)
)
    resume = Resume(
        user_id=current_user.id,
        filename=unique_filename,
        original_filename=file.filename,
        filepath=str(file_path),
        extracted_text=extracted_text
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": resume.filename,
        "uploaded_by": current_user.email
    }
    
@router.get(
    "",
    response_model=list[ResumeResponse]
)
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resumes = (
    db.query(Resume)
    .filter(
        Resume.user_id == current_user.id
    )
    .all()
)

    return resumes
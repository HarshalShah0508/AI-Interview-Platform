import json

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from app.services.resume_analysis_worker import (
    ResumeAnalysisWorker,
)
from app.services.evidence_validator import (
    EvidenceValidator,
)
from app.services.recommendation_engine import (
    RecommendationEngine,
)
from app.services.resume_optimizer import (
    ResumeOptimizer,
)
from sqlalchemy.orm import Session
from app.services.resume_analyzer import ResumeAnalyzer
from app.api.auth import get_current_user
from app.core.config import GEMINI_MODEL
from app.database.database import get_db
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.user import User
from app.services.job_description_parser import (
    JobDescriptionParser,
)
from app.schemas.resume_analysis import (
    JDProfile,
    ResumeProfile,
    MatchingReport,
)

from app.services.requirement_matcher import (
    RequirementMatcher,
)

router = APIRouter(
    prefix="/resume-analysis",
    tags=["Resume Analysis"],
)


@router.post("/analyze-jd")
async def analyze_job_description(
    resume_id: int = Form(...),
    job_description: str | None = Form(None),
    job_description_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Phase 1:

    Extract and structure a job description
    against an existing user's resume.

    Matching and optimization will be added
    in subsequent phases.
    """

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    if not job_description and not job_description_file:

        raise HTTPException(
            status_code=400,
            detail=(
                "Provide either job description "
                "text or a job description file."
            ),
        )

    try:

        parser = JobDescriptionParser()

        extracted_jd = (
            await parser.extract_job_description(
                text=job_description,
                file=job_description_file,
            )
        )

        jd_profile = (
            parser.structure_job_description(
                extracted_jd
            )
        )
        resume_analyzer = ResumeAnalyzer()

        resume_profile = resume_analyzer.analyze(
            resume.extracted_text
        )
        validator = EvidenceValidator()

        resume_profile = validator.validate(
            resume_text=resume.extracted_text,
            profile=resume_profile,
        )
        matcher = RequirementMatcher()

        matching_report = matcher.match(
            jd_profile=jd_profile,
            resume_profile=resume_profile,
        )
        analysis_result = {
            "resume_profile": resume_profile.model_dump(),

            "matching_report": (
                matching_report.model_dump()
            ),

            "optimization_report": (
                optimization_report.model_dump()
            ),
            "recommendation_report": (
                recommendation_report.model_dump()
            )
        }
        optimizer = ResumeOptimizer()

        optimization_report = optimizer.analyze(
            jd_profile=jd_profile,
            resume_profile=resume_profile,
            matching_report=matching_report,
        )
        recommendation_engine = (
            RecommendationEngine()
        )

        recommendation_report = (
            recommendation_engine.generate(
                jd_profile=jd_profile,
                resume_profile=resume_profile,
                matching_report=matching_report,
                optimization_report=optimization_report,
            )
        )

        analysis = ResumeAnalysis(
            user_id=current_user.id,
            resume_id=resume.id,
            job_description_text=extracted_jd,
            job_title=jd_profile.job_title,
            jd_profile_json=jd_profile.model_dump_json(),
            analysis_result_json=json.dumps(
                analysis_result
            ),
            overall_score=round(
                matching_report.overall_score
            ),
        )

        db.add(analysis)

        db.commit()

        db.refresh(analysis)

        return {
            "analysis_id": analysis.id,
            "resume_id": resume.id,
            "job_title": jd_profile.job_title,

            "jd_profile": jd_profile.model_dump(),

            "resume_profile": (
                resume_profile.model_dump()
            ),

            "matching_report": (
                matching_report.model_dump()
           ),

            "optimization_report": (
                optimization_report.model_dump()
            ),
            "recommendation_report": (
                recommendation_report.model_dump()
            ),
            "message": (
                "Job description and resume "
                "successfully analyzed."
            ),
        }

    except ValueError as exc:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to analyze the "
                "job description."
            ),
        ) from exc

@router.post("/start")
async def start_resume_analysis(
    background_tasks: BackgroundTasks,

    resume_id: int = Form(...),

    job_description: str | None = Form(
        None
    ),

    job_description_file: UploadFile | None = File(
        None
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Creates a resume-JD analysis job.

    The heavy analysis runs in the background.
    """

    # --------------------------------------------------------
    # Validate resume ownership
    # --------------------------------------------------------

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    # --------------------------------------------------------
    # Validate JD input
    # --------------------------------------------------------

    if (
        not job_description
        and not job_description_file
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Provide either job description "
                "text or a job description file."
            ),
        )

    # --------------------------------------------------------
    # Extract JD immediately.
    #
    # We need the actual text stored in the database
    # before the request ends.
    # --------------------------------------------------------

    parser = JobDescriptionParser()

    try:

        extracted_jd = (
            await parser.extract_job_description(
                text=job_description,
                file=job_description_file,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # --------------------------------------------------------
    # Create analysis record
    # --------------------------------------------------------

    analysis = ResumeAnalysis(
        user_id=current_user.id,

        resume_id=resume.id,

        job_description_text=extracted_jd,

        status="processing",

        progress=0,

        current_stage=(
            "Analysis queued"
        ),
    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    # --------------------------------------------------------
    # Start background worker
    # --------------------------------------------------------

    background_tasks.add_task(
        ResumeAnalysisWorker(
            analysis.id
        ).run
    )

    return {
        "analysis_id": analysis.id,

        "status": analysis.status,

        "progress": analysis.progress,

        "current_stage": (
            analysis.current_stage
        ),

        "message": (
            "Resume analysis started."
        ),
    }
    
@router.get("/{analysis_id}/status")
def get_analysis_status(
    analysis_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):
    analysis = (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.id
            == analysis_id,

            ResumeAnalysis.user_id
            == current_user.id,
        )
        .first()
    )

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    return {
        "analysis_id": analysis.id,

        "status": analysis.status,

        "progress": analysis.progress,

        "current_stage": (
            analysis.current_stage
        ),

        "error_message": (
            analysis.error_message
        ),

        "overall_score": (
            analysis.overall_score
        ),

        "created_at": (
            analysis.created_at
        ),

        "completed_at": (
            analysis.completed_at
        ),
    }

@router.get("/{analysis_id}/result")
def get_analysis_result(
    analysis_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):
    analysis = (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.id
            == analysis_id,

            ResumeAnalysis.user_id
            == current_user.id,
        )
        .first()
    )

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    if analysis.status == "processing":

        raise HTTPException(
            status_code=202,
            detail={
                "message": (
                    "Analysis is still processing."
                ),
                "progress": (
                    analysis.progress
                ),
            },
        )

    if analysis.status == "failed":

        raise HTTPException(
            status_code=500,
            detail=(
                analysis.error_message
                or "Analysis failed."
            ),
        )

    if not analysis.analysis_result_json:

        raise HTTPException(
            status_code=500,
            detail=(
                "Analysis completed without "
                "a result."
            ),
        )

    try:

        result = json.loads(
            analysis.analysis_result_json
        )

    except json.JSONDecodeError as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Stored analysis result is invalid."
            ),
        ) from exc

    return {
        "analysis_id": analysis.id,

        "status": analysis.status,

        "overall_score": (
            analysis.overall_score
        ),

        "job_title": analysis.job_title,

        "result": result,
    }
        
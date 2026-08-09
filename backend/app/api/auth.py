from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from sqlalchemy.orm import Session
from fastapi import Query
from app.database.database import get_db
from app.models.user import User
from app.services.email_service import EmailService
from app.schemas.user import (
    UserCreate,
    UserResponse,
    GoogleLoginRequest
)
from app.services.email_verification_service import (
    EmailVerificationService,
)
from app.utils.security import (
    hash_password,
    verify_password
)
from app.schemas.user import ResendVerificationRequest
from app.utils.jwt_handler import (
    create_access_token,
    get_current_user
)

from app.services.oauth_service import (
    authenticate_google_user
)

router = APIRouter()


@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(
            user.password
        ),
        auth_provider="local",
        email_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verification_token = (
        EmailVerificationService.generate_verification_token(
            db=db,
            user_id=new_user.id,
        )
    )

    EmailService().send_verification_email(
        recipient_email=new_user.email,
        recipient_name=new_user.username,
        verification_token=verification_token,
    )

    return {
        "message":
            "Account created successfully. Please check your email to verify your account."
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if user.hashed_password is None:
        raise HTTPException(
            status_code=401,
            detail="This account was created using Google Sign-In. Please continue with Google."
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    if (
    user.auth_provider == "local"
    and not user.email_verified
):
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in."
    )

    access_token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/auth/google")
def google_auth(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    return authenticate_google_user(
        request.id_token,
        db
    )
@router.get("/auth/verify-email")
def verify_email(
    token: str = Query(...),
    db: Session = Depends(get_db),
):

    user = EmailVerificationService.verify_token(
        db=db,
        token=token,
    )

    return {
        "message": "Email verified successfully.",
        "email": user.email,
    }
@router.post("/auth/resend-verification")
def resend_verification_email(
    request: ResendVerificationRequest,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    # Never reveal whether the email exists
    if (
        user is None
        or user.auth_provider != "local"
        or user.email_verified
    ):
        return {
            "message": (
                "If your account requires verification, "
                "a verification email has been sent."
            )
        }

    verification_token = (
        EmailVerificationService.generate_verification_token(
            db=db,
            user_id=user.id,
        )
    )

    EmailService().send_verification_email(
        recipient_email=user.email,
        recipient_name=user.username,
        verification_token=verification_token,
    )

    return {
        "message": (
            "If your account requires verification, "
            "a verification email has been sent."
        )
    }
@router.get(
    "/me",
    response_model=UserResponse
)
def read_me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user
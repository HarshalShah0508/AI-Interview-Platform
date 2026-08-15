from datetime import datetime, timedelta
import hashlib
import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.email_verification_token import (
    EmailVerificationToken,
)
from app.models.user import User


class EmailVerificationService:

    TOKEN_EXPIRY_HOURS = 24

    @staticmethod
    def generate_verification_token(
        db: Session,
        user_id: int,
    ) -> str:
        """
        Generates a secure verification token,
        stores its SHA-256 hash in the database,
        and returns the original token.
        """

        db.query(
            EmailVerificationToken
        ).filter(
            EmailVerificationToken.user_id == user_id
        ).delete()

        token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        verification_token = EmailVerificationToken(
            user_id=user_id,
            token=token_hash,
            expires_at=datetime.utcnow()
            + timedelta(
                hours=EmailVerificationService.TOKEN_EXPIRY_HOURS
            ),
        )

        db.add(verification_token)
        db.commit()

        return token

    @staticmethod
    def hash_token(
        token: str,
    ) -> str:

        return hashlib.sha256(
            token.encode()
        ).hexdigest()

    @staticmethod
    def verify_token(
        db: Session,
        token: str,
    ) -> User:
        """
        Verifies a verification token.

        Returns the associated user if valid.
        """

        token_hash = EmailVerificationService.hash_token(
            token
        )

        verification_record = (
            db.query(
                EmailVerificationToken
            )
            .filter(
                EmailVerificationToken.token == token_hash
            )
            .first()
        )

        if verification_record is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid verification token."
            )

        if verification_record.expires_at < datetime.utcnow():

            db.delete(verification_record)
            db.commit()

            raise HTTPException(
                status_code=400,
                detail="Verification token has expired."
            )

        user = (
            db.query(User)
            .filter(
                User.id == verification_record.user_id
            )
            .first()
        )

        if user is None:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        user.email_verified = True

        db.delete(
            verification_record
        )

        db.commit()
        db.refresh(user)

        return user
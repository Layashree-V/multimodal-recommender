from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib
import secrets

from app.database.connection import get_db
from app.models.user import User

router = APIRouter()


# ---------------------------------------------------------
# Password helpers
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Creates a secure salted password hash.
    """
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return f"pbkdf2_sha256${salt}${password_hash}"


def verify_password(password: str, stored_password: str) -> bool:
    """
    Supports both:
    1. New hashed passwords
    2. Old plain-text passwords already stored in your DB

    Old plain-text passwords are supported so your existing
    Tester account does not suddenly stop working.
    """

    if not stored_password:
        return False

    # New hashed password
    if stored_password.startswith("pbkdf2_sha256$"):
        try:
            _, salt, expected_hash = stored_password.split("$")

            actual_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                100_000
            ).hex()

            return secrets.compare_digest(
                actual_hash,
                expected_hash
            )

        except ValueError:
            return False

    # Legacy plain-text password
    return secrets.compare_digest(
        password,
        stored_password
    )


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

from pydantic import BaseModel, EmailStr


class AuthRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


# ---------------------------------------------------------
# SIGNUP
# ---------------------------------------------------------

@router.post("/signup")
def signup(
    request: AuthRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=request.name,
        email=request.email,
        password=hash_password(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


# ---------------------------------------------------------
# SIGNIN
# ---------------------------------------------------------

@router.post("/signin")
def signin(
    request: AuthRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        request.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # If the old password was plain text,
    # convert it to a secure hash after successful login.
    if not user.password.startswith("pbkdf2_sha256$"):
        user.password = hash_password(request.password)
        db.commit()

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }
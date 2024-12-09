from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.auth import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.token import Token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Log login attempt
    logger.info(f"Login attempt for username: {form_data.username}")
    
    # Find user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        logger.warning(f"User not found: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Invalid password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    logger.info(f"Login successful for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
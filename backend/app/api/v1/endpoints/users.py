from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.core.auth import get_password_hash, get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=UserSchema)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        # Check if user exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user with properly hashed password
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=True,
            is_superuser=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: UserSchema = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    user_update: UserUpdate,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user
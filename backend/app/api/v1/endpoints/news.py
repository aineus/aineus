from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas import schemas
from app.core.news_engine import NewsEngine
from app.core.auth import get_optional_current_user  # Changed to optional auth

router = APIRouter()

@router.get("/", response_model=List[schemas.News])
async def get_news(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[schemas.User] = Depends(get_optional_current_user)  # Made optional
):
    """Get list of news articles"""
    news_engine = NewsEngine(db)
    return await news_engine.get_news(skip=skip, limit=limit, category=category)
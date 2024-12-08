from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.database import get_db
from app.schemas import news as news_schemas
from app.schemas.user import User  # Changed to direct import
from app.models.news import News, Category, news_categories, news_prompts
from app.models.prompt import Prompt
from app.core.news_engine import NewsEngine
from app.services.news_collector import NewsCollector
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/prompt/{prompt_id}", response_model=List[news_schemas.NewsInPrompt])
async def get_prompt_news(
    prompt_id: int,
    skip: int = 0,
    limit: int = 10,
    refresh: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Using directly imported User
):
    """Get news for a specific prompt-newspaper"""
    
    # Verify prompt access
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    if not prompt.is_public and prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this prompt's news"
        )

    # Initialize collector
    collector = NewsCollector(db)
    
    # Refresh news if requested
    if refresh:
        await collector.collect_news_for_prompt(prompt_id)
    
    # Get news with prompt-specific metadata
    news_items = db.query(News).join(
        news_prompts
    ).filter(
        news_prompts.c.prompt_id == prompt_id
    ).order_by(
        news_prompts.c.display_order
    ).offset(skip).limit(limit).all()
    
    return news_items

@router.get("/prompt/{prompt_id}/categories", response_model=List[str])
async def get_prompt_categories(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available categories in a prompt-newspaper"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt or (not prompt.is_public and prompt.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found or access denied"
        )
    
    # Get unique categories for this prompt's news
    categories = db.query(Category.name).distinct().join(
        news_categories
    ).join(
        News
    ).join(
        news_prompts
    ).filter(
        news_prompts.c.prompt_id == prompt_id
    ).all()
    
    return [cat[0] for cat in categories]

@router.get("/prompt/{prompt_id}/category/{category}", response_model=List[news_schemas.NewsInPrompt])
async def get_prompt_news_by_category(
    prompt_id: int,
    category: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get category-specific news from a prompt-newspaper"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt or (not prompt.is_public and prompt.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found or access denied"
        )
    
    news_items = db.query(News).join(
        news_prompts
    ).join(
        news_categories
    ).join(
        Category
    ).filter(
        news_prompts.c.prompt_id == prompt_id,
        Category.slug == category
    ).order_by(
        news_prompts.c.display_order
    ).offset(skip).limit(limit).all()
    
    return news_items

@router.post("/prompt/{prompt_id}/refresh", response_model=dict)
async def refresh_prompt_news(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually refresh news for a prompt-newspaper"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt or (not prompt.is_public and prompt.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found or access denied"
        )
    
    collector = NewsCollector(db)
    await collector.collect_news_for_prompt(prompt_id)
    
    return {"status": "success", "message": "News refreshed successfully"}
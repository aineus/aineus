from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.database import get_db
from app.schemas import prompt as prompt_schemas
from app.schemas import user as user_schemas
from app.models.prompt import Prompt, Tag
from app.models.news import News, Category, news_categories, news_prompts
from app.core.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=prompt_schemas.Prompt)
async def create_prompt(
    prompt: prompt_schemas.PromptCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(get_current_user)
):
    """Create a new prompt-newspaper"""
    db_prompt = Prompt(
        name=prompt.name,
        description=prompt.description,
        prompt_text=prompt.prompt_text,
        system_prompt=prompt.system_prompt,
        is_public=prompt.is_public,
        refresh_interval=prompt.refresh_interval,
        max_articles=prompt.max_articles,
        custom_categories=prompt.custom_categories,
        source_preferences=prompt.source_preferences,
        llm_provider=prompt.llm_provider,
        llm_config=prompt.llm_config,
        layout_settings=prompt.layout_settings,
        sorting_preferences=prompt.sorting_preferences,
        meta_info=prompt.meta_info,
        user_id=current_user.id
    )
    
    if prompt.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(prompt.tag_ids)).all()
        db_prompt.tags = tags
    
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.get("/", response_model=List[prompt_schemas.PromptNewspaper])
async def read_prompts(
    skip: int = 0,
    limit: int = 10,
    include_stats: bool = False,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(get_current_user)
):
    """Get all prompt-newspapers for current user"""
    prompts = db.query(Prompt).filter(
        (Prompt.user_id == current_user.id) | (Prompt.is_public == True)
    ).offset(skip).limit(limit).all()
    
    if include_stats:
        for prompt in prompts:
            # Add newspaper statistics
            prompt.total_articles = db.query(func.count(news_prompts.c.news_id)).filter(
                news_prompts.c.prompt_id == prompt.id
            ).scalar()
            
            # Get latest refresh time
            prompt.latest_refresh = db.query(func.max(News.created_at)).join(
                news_prompts
            ).filter(
                news_prompts.c.prompt_id == prompt.id
            ).scalar() or prompt.created_at
            
            # Get category summary
            categories = db.query(
                Category.name,
                func.count(news_categories.c.news_id).label('count')
            ).join(
                news_categories
            ).join(
                News
            ).join(
                news_prompts
            ).filter(
                news_prompts.c.prompt_id == prompt.id
            ).group_by(
                Category.name
            ).all()
            
            prompt.categories_summary = {cat.name: cat.count for cat in categories}
    
    return prompts

@router.get("/{prompt_id}", response_model=prompt_schemas.PromptNewspaper)
async def read_prompt(
    prompt_id: int,
    include_stats: bool = False,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(get_current_user)
):
    """Get a specific prompt-newspaper"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    if not prompt.is_public and prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this prompt"
        )
    
    if include_stats:
        # Add newspaper statistics (same as in read_prompts)
        prompt.total_articles = db.query(func.count(news_prompts.c.news_id)).filter(
            news_prompts.c.prompt_id == prompt.id
        ).scalar()
        
        prompt.latest_refresh = db.query(func.max(News.created_at)).join(
            news_prompts
        ).filter(
            news_prompts.c.prompt_id == prompt.id
        ).scalar() or prompt.created_at
        
        categories = db.query(
            Category.name,
            func.count(news_categories.c.news_id).label('count')
        ).join(
            news_categories
        ).join(
            News
        ).join(
            news_prompts
        ).filter(
            news_prompts.c.prompt_id == prompt.id
        ).group_by(
            Category.name
        ).all()
        
        prompt.categories_summary = {cat.name: cat.count for cat in categories}
    
    return prompt

@router.put("/{prompt_id}", response_model=prompt_schemas.Prompt)
async def update_prompt(
    prompt_id: int,
    prompt_update: prompt_schemas.PromptUpdate,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(get_current_user)
):
    """Update a prompt-newspaper"""
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    if db_prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this prompt"
        )
    
    # Update prompt fields
    for key, value in prompt_update.dict(exclude_unset=True).items():
        if key == 'tag_ids' and value is not None:
            tags = db.query(Tag).filter(Tag.id.in_(value)).all()
            db_prompt.tags = tags
        else:
            setattr(db_prompt, key, value)
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(get_current_user)
):
    """Delete a prompt-newspaper"""
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    if db_prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this prompt"
        )
    
    db.delete(db_prompt)
    db.commit()
    
    return {"message": "Prompt-newspaper deleted successfully"}
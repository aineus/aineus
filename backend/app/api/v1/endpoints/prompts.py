from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas import schemas
from app.models.prompt import Prompt
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Prompt)
async def create_prompt(
    prompt: schemas.PromptCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Create a new prompt"""
    db_prompt = Prompt(
        name=prompt.name,
        description=prompt.description,
        prompt_text=prompt.prompt_text,
        system_prompt=prompt.system_prompt,
        is_public=prompt.is_public,
        llm_provider=prompt.llm_provider,
        llm_config=prompt.llm_config,
        user_id=current_user.id
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.get("/", response_model=List[schemas.Prompt])
async def read_prompts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get all prompts for current user"""
    prompts = db.query(Prompt).filter(
        (Prompt.user_id == current_user.id) | (Prompt.is_public == True)
    ).offset(skip).limit(limit).all()
    return prompts

@router.get("/{prompt_id}", response_model=schemas.Prompt)
async def read_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get a specific prompt"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Check if user has access to this prompt
    if not prompt.is_public and prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this prompt"
        )
    
    return prompt

@router.put("/{prompt_id}", response_model=schemas.Prompt)
async def update_prompt(
    prompt_id: int,
    prompt_update: schemas.PromptBase,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Update a prompt"""
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Check if user owns this prompt
    if db_prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this prompt"
        )
    
    # Update prompt fields
    for key, value in prompt_update.dict(exclude_unset=True).items():
        setattr(db_prompt, key, value)
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete a prompt"""
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Check if user owns this prompt
    if db_prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this prompt"
        )
    
    db.delete(db_prompt)
    db.commit()
    
    return {"message": "Prompt deleted successfully"}
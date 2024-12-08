from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .news import NewsInPrompt  # Import NewsInPrompt from news schema

class TagBase(BaseModel):
    name: str
    slug: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

class PromptBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_text: str
    system_prompt: Optional[str] = None
    is_public: bool = False
    
    # Newspaper specific settings
    refresh_interval: int = Field(24, ge=1, description="Refresh interval in hours")
    max_articles: int = Field(100, ge=1, le=1000)
    custom_categories: Optional[Dict[str, Any]] = None
    source_preferences: Optional[Dict[str, Any]] = None
    
    # LLM configuration
    llm_provider: Optional[str] = None
    llm_config: Optional[Dict[str, Any]] = None
    
    # Layout and presentation settings
    layout_settings: Optional[Dict[str, Any]] = None
    sorting_preferences: Optional[Dict[str, Any]] = None
    
    meta_info: Optional[Dict[str, Any]] = None

class PromptCreate(PromptBase):
    tag_ids: Optional[List[int]] = []

class PromptUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    prompt_text: Optional[str] = None
    system_prompt: Optional[str] = None
    is_public: Optional[bool] = None
    refresh_interval: Optional[int] = Field(None, ge=1)
    max_articles: Optional[int] = Field(None, ge=1, le=1000)
    custom_categories: Optional[Dict[str, Any]] = None
    source_preferences: Optional[Dict[str, Any]] = None
    llm_provider: Optional[str] = None
    llm_config: Optional[Dict[str, Any]] = None
    layout_settings: Optional[Dict[str, Any]] = None
    sorting_preferences: Optional[Dict[str, Any]] = None
    meta_info: Optional[Dict[str, Any]] = None
    tag_ids: Optional[List[int]] = None

class Prompt(PromptBase):
    id: int
    user_id: int
    tags: List[Tag] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PromptNewspaper(Prompt):
    total_articles: int = 0
    latest_refresh: datetime
    categories_summary: Dict[str, int] = {}
    news_items: List[NewsInPrompt] = []
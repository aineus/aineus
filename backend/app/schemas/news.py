from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class NewsTransformationBase(BaseModel):
    transformed_content: str
    llm_provider: str
    transformation_type: Optional[str] = None
    quality_score: Optional[float] = None
    processing_time: Optional[float] = None
    meta_info: Optional[Dict[str, Any]] = None

class NewsTransformationCreate(NewsTransformationBase):
    news_id: int
    prompt_id: int

class NewsTransformation(NewsTransformationBase):
    id: int
    news_id: int
    prompt_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    source: str
    url: Optional[HttpUrl] = None
    published_at: datetime
    image_url: Optional[HttpUrl] = None
    author: Optional[str] = None
    read_time: Optional[int] = Field(None, description="Estimated reading time in minutes")
    importance_score: Optional[float] = Field(None, ge=0, le=1)
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1)
    meta_info: Optional[Dict[str, Any]] = None

class NewsCreate(NewsBase):
    raw_data: Optional[Dict[str, Any]] = None
    category_ids: List[int] = []

class News(NewsBase):
    id: int
    raw_data: Optional[Dict[str, Any]] = None
    categories: List[Category] = []
    transformations: List[NewsTransformation] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsInPrompt(News):
    relevance_score: Optional[float] = Field(None, ge=0, le=1)
    display_order: Optional[int] = None
    prompt_specific_meta: Optional[Dict[str, Any]] = None
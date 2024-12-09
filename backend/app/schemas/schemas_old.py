from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# News Schemas
class NewsBase(BaseModel):
    title: str
    content: str
    source: str
    summary: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None

class NewsCreate(NewsBase):
    published_at: datetime
    categories: List[str]
    raw_data: Optional[Dict[str, Any]] = None

class News(NewsBase):
    id: int
    published_at: datetime
    created_at: datetime
    updated_at: datetime
    categories: List[str]

    class Config:
        from_attributes = True

# Prompt Schemas
class PromptBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_text: str
    system_prompt: Optional[str] = None
    is_public: bool = False
    llm_provider: Optional[str] = "openai"
    llm_config: Optional[Dict[str, Any]] = None

class PromptCreate(PromptBase):
    user_id: int

class PromptUpdate(PromptBase):
    pass

class Prompt(PromptBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Transformation Schemas
class TransformationBase(BaseModel):
    news_id: int
    prompt_id: int

class TransformationCreate(TransformationBase):
    pass

class Transformation(TransformationBase):
    id: int
    transformed_content: str
    llm_provider: str
    meta_info: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
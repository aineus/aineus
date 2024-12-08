from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# News schemas
class NewsBase(BaseModel):
    title: str
    content: str
    source: str
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

class NewsCreate(NewsBase):
    published_at: datetime
    categories: List[str]
    raw_data: Optional[Dict[str, Any]] = None

class News(NewsBase):
    id: int
    summary: Optional[str] = None
    published_at: datetime
    created_at: datetime
    updated_at: datetime
    categories: List[str]

    class Config:
        from_attributes = True

# Prompt schemas
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

class Prompt(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True

# Response schemas
class ResponseBase(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(ResponseBase):
    error_code: str
    details: Optional[Dict[str, Any]] = None
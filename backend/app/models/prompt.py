from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Prompt(Base, TimestampMixin):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    prompt_text = Column(Text, nullable=False)
    system_prompt = Column(Text)
    is_public = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # LLM configuration
    llm_provider = Column(String)  # openai, llama, mistral
    llm_config = Column(JSON)  # Store model-specific configuration
    
    # Metadata (renamed to avoid conflict)
    meta_info = Column(JSON)  # Changed from metadata to meta_info
    
    # Relationships
    user = relationship("User", back_populates="prompts")
    transformations = relationship("NewsTransformation", back_populates="prompt")

class UserNewsPreference(Base, TimestampMixin):
    __tablename__ = "user_news_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    default_prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=True)
    
    # News preferences
    preferred_categories = Column(JSON)  # List of category IDs
    excluded_sources = Column(JSON)  # List of source names to exclude
    update_frequency = Column(Integer, default=24)  # Hours
    
    # Relationships
    user = relationship("User", back_populates="news_preferences")
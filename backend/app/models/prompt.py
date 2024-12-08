from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON, Table
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

# Many-to-many relationship for prompt tags
prompt_tags = Table(
    'prompt_tags',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Prompt(Base, TimestampMixin):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    prompt_text = Column(Text, nullable=False)
    system_prompt = Column(Text)
    is_public = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Newspaper specific settings
    refresh_interval = Column(Integer, default=24)  # Hours
    max_articles = Column(Integer, default=100)
    custom_categories = Column(JSON)  # User-defined categories for this newspaper
    source_preferences = Column(JSON)  # Preferred/excluded sources
    
    # LLM configuration
    llm_provider = Column(String)  # openai, llama, mistral
    llm_config = Column(JSON)  # Store model-specific configuration
    
    # Layout and presentation settings
    layout_settings = Column(JSON)  # Store layout preferences
    sorting_preferences = Column(JSON)  # How articles should be sorted/organized
    
    # Metadata
    meta_info = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="prompts")
    transformations = relationship("NewsTransformation", back_populates="prompt")
    tags = relationship("Tag", secondary=prompt_tags, back_populates="prompts")
    news_items = relationship("News", secondary="news_prompts", back_populates="prompts")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    
    # Relationships
    prompts = relationship("Prompt", secondary=prompt_tags, back_populates="tags")

class UserNewsPreference(Base, TimestampMixin):
    __tablename__ = "user_news_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    default_prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=True)
    
    # Global news preferences
    global_excluded_sources = Column(JSON)  # List of source names to exclude
    global_settings = Column(JSON)  # Any global settings for news consumption
    
    # Relationships
    user = relationship("User", back_populates="news_preferences")
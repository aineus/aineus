from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

# Many-to-many relationship table for news categories
news_categories = Table(
    'news_categories',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class News(Base, TimestampMixin):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    source = Column(String, nullable=False)
    url = Column(String)
    published_at = Column(DateTime, nullable=False)
    image_url = Column(String)
    
    # Store original data and metadata - renamed to avoid conflict
    raw_data = Column(JSON)
    meta_info = Column(JSON)  # Changed from metadata to meta_info

    # Relationships
    categories = relationship("Category", secondary=news_categories, back_populates="news_items")
    transformations = relationship("NewsTransformation", back_populates="news")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    
    # Relationships
    news_items = relationship("News", secondary=news_categories, back_populates="categories")

class NewsTransformation(Base, TimestampMixin):
    __tablename__ = "news_transformations"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    transformed_content = Column(Text, nullable=False)
    llm_provider = Column(String, nullable=False)
    meta_info = Column(JSON)  # Changed from metadata to meta_info

    # Relationships
    news = relationship("News", back_populates="transformations")
    prompt = relationship("Prompt", back_populates="transformations")
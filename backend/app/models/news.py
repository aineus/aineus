from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, JSON, Float
from sqlalchemy.orm import relationship, backref
from .base import Base, TimestampMixin

# Many-to-many relationship table for news categories
news_categories = Table(
    'news_categories',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# Many-to-many relationship table for news prompts
news_prompts = Table(
    'news_prompts',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('prompt_id', Integer, ForeignKey('prompts.id')),
    Column('display_order', Integer, nullable=True)
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    # Fix the self-referential relationship
    children = relationship(
        'Category',
        backref=backref('parent', remote_side=[id]),
        cascade='all, delete-orphan'
    )
    
    # News relationship
    news_items = relationship("News", secondary=news_categories, back_populates="categories")

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
    
    author = Column(String)
    read_time = Column(Integer)
    importance_score = Column(Float)
    sentiment_score = Column(Float)
    
    raw_data = Column(JSON)
    meta_info = Column(JSON)

    # Relationships
    categories = relationship("Category", secondary=news_categories, back_populates="news_items")
    transformations = relationship("NewsTransformation", back_populates="news")
    prompts = relationship("Prompt", secondary=news_prompts, back_populates="news_items")

class NewsTransformation(Base, TimestampMixin):
    __tablename__ = "news_transformations"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    transformed_content = Column(Text, nullable=False)
    llm_provider = Column(String, nullable=False)
    
    transformation_type = Column(String)
    quality_score = Column(Float)
    processing_time = Column(Float)
    meta_info = Column(JSON)

    # Relationships
    news = relationship("News", back_populates="transformations")
    prompt = relationship("Prompt", back_populates="transformations")
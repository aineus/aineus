from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, JSON, Float
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

# Many-to-many relationship table for news categories
news_categories = Table(
    'news_categories',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# Many-to-many relationship table for news-prompts
news_prompts = Table(
    'news_prompts',
    Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('prompt_id', Integer, ForeignKey('prompts.id')),
    Column('relevance_score', Float),  # How relevant this news is for this prompt
    Column('display_order', Integer),  # Order in the prompt's newspaper
    Column('meta_info', JSON)  # Prompt-specific metadata for this news item
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
    
    # Enhanced metadata
    author = Column(String)
    read_time = Column(Integer)  # Estimated reading time in minutes
    importance_score = Column(Float)  # Global importance score
    sentiment_score = Column(Float)  # Sentiment analysis result
    
    # Store original data and metadata
    raw_data = Column(JSON)
    meta_info = Column(JSON)

    # Relationships
    categories = relationship("Category", secondary=news_categories, back_populates="news_items")
    transformations = relationship("NewsTransformation", back_populates="news")
    prompts = relationship("Prompt", secondary=news_prompts, back_populates="news_items")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    # Relationships
    news_items = relationship("News", secondary=news_categories, back_populates="categories")
    children = relationship(
        "Category",
        backref=relationship("Category", remote_side=[id]),
        primaryjoin=(id == parent_id),
        cascade="all, delete-orphan"
    )



class NewsTransformation(Base, TimestampMixin):
    __tablename__ = "news_transformations"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    transformed_content = Column(Text, nullable=False)
    llm_provider = Column(String, nullable=False)
    
    # Enhanced transformation metadata
    transformation_type = Column(String)  # Type of transformation performed
    quality_score = Column(Float)  # Quality assessment of transformation
    processing_time = Column(Float)  # Time taken for transformation
    meta_info = Column(JSON)

    # Relationships
    news = relationship("News", back_populates="transformations")
    prompt = relationship("Prompt", back_populates="transformations")
from sqlalchemy.orm import Session
from app.models.news import News, Category, NewsTransformation
from app.models.prompt import Prompt
from app.core.llm.factory import LLMFactory
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class NewsEngine:
    def __init__(self, db: Session):
        self.db = db
        self.llm_factory = LLMFactory()

    async def get_news(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None
    ) -> List[News]:
        query = self.db.query(News)
        
        if category:
            query = query.join(News.categories).filter(Category.slug == category)
        
        return query.offset(skip).limit(limit).all()

    async def transform_news(
        self,
        news_id: int,
        prompt_id: int
    ) -> NewsTransformation:
        news = self.db.query(News).filter(News.id == news_id).first()
        prompt = self.db.query(Prompt).filter(Prompt.id == prompt_id).first()
        
        if not news or not prompt:
            raise ValueError("News or prompt not found")

        # Get appropriate LLM
        llm = self.llm_factory.create(provider=prompt.llm_provider)
        
        # Transform content
        response = await llm.generate(
            prompt=prompt.prompt_text,
            system_prompt=prompt.system_prompt,
            content=news.content
        )

        # Create transformation record
        transformation = NewsTransformation(
            news_id=news_id,
            prompt_id=prompt_id,
            transformed_content=response.content,
            llm_provider=prompt.llm_provider,
            metadata=response.metadata
        )
        
        self.db.add(transformation)
        self.db.commit()
        self.db.refresh(transformation)
        
        return transformation
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging
from app.models.news import News, Category, NewsTransformation, news_prompts
from app.models.prompt import Prompt
from app.core.llm.factory import LLMFactory
from sqlalchemy import and_, or_, func

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self, db: Session):
        self.db = db
        self.llm_factory = LLMFactory()

    async def collect_news_for_prompt(self, prompt_id: int) -> List[News]:
        """
        Collects and processes news for a specific prompt-newspaper
        """
        prompt = self.db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")

        # Check if refresh is needed
        last_refresh = self._get_last_refresh_time(prompt_id)
        if last_refresh and datetime.utcnow() - last_refresh < timedelta(hours=prompt.refresh_interval):
            logger.info(f"Skipping refresh for prompt {prompt_id} - within refresh interval")
            return self._get_existing_news_for_prompt(prompt_id)

        # Collect raw news based on prompt preferences
        raw_news = await self._collect_raw_news(prompt)
        
        # Process and organize news
        processed_news = await self._process_news_for_prompt(raw_news, prompt)
        
        # Store and organize in database
        return await self._store_news_for_prompt(processed_news, prompt)

    async def _collect_raw_news(self, prompt: Prompt) -> List[Dict[str, Any]]:
        """
        Collects raw news based on prompt preferences
        """
        # Implementation would depend on your news sources
        # This is a placeholder for the actual implementation
        # You would typically:
        # 1. Call external news APIs
        # 2. Scrape news websites
        # 3. Aggregate from multiple sources
        pass

    async def _process_news_for_prompt(
        self, 
        raw_news: List[Dict[str, Any]], 
        prompt: Prompt
    ) -> List[Dict[str, Any]]:
        """
        Processes raw news using the prompt's LLM configuration
        """
        llm = self.llm_factory.create(provider=prompt.llm_provider)
        processed_news = []

        for news_item in raw_news:
            try:
                # Transform content using prompt
                transformed = await llm.generate(
                    prompt=prompt.prompt_text,
                    system_prompt=prompt.system_prompt,
                    content=news_item['content']
                )

                # Calculate relevance score
                relevance_score = await self._calculate_relevance_score(
                    news_item, 
                    transformed.content, 
                    prompt
                )

                # Process metadata
                meta_info = await self._process_metadata(news_item, transformed, prompt)

                processed_news.append({
                    'raw_data': news_item,
                    'transformed_content': transformed.content,
                    'relevance_score': relevance_score,
                    'meta_info': meta_info
                })

            except Exception as e:
                logger.error(f"Error processing news item: {e}")
                continue

        return processed_news

    async def _store_news_for_prompt(
        self, 
        processed_news: List[Dict[str, Any]], 
        prompt: Prompt
    ) -> List[News]:
        """
        Stores processed news in the database and associates with prompt
        """
        stored_news = []
        display_order = 1

        for news_data in processed_news:
            try:
                # Create or update news entry
                news_item = self._create_or_update_news(news_data)
                
                # Create transformation record
                transformation = NewsTransformation(
                    news_id=news_item.id,
                    prompt_id=prompt.id,
                    transformed_content=news_data['transformed_content'],
                    llm_provider=prompt.llm_provider,
                    meta_info=news_data['meta_info']
                )

                # Associate with prompt
                stmt = news_prompts.insert().values(
                    news_id=news_item.id,
                    prompt_id=prompt.id,
                    relevance_score=news_data['relevance_score'],
                    display_order=display_order,
                    meta_info=news_data['meta_info']
                )

                self.db.execute(stmt)
                self.db.add(transformation)
                stored_news.append(news_item)
                display_order += 1

            except Exception as e:
                logger.error(f"Error storing news item: {e}")
                continue

        self.db.commit()
        return stored_news

    def _create_or_update_news(self, news_data: Dict[str, Any]) -> News:
        """
        Creates or updates a news entry in the database
        """
        raw_data = news_data['raw_data']
        existing_news = self.db.query(News).filter(
            News.url == raw_data['url']
        ).first()

        if existing_news:
            return existing_news

        news_item = News(
            title=raw_data['title'],
            content=raw_data['content'],
            summary=raw_data.get('summary'),
            source=raw_data['source'],
            url=raw_data['url'],
            published_at=raw_data['published_at'],
            image_url=raw_data.get('image_url'),
            author=raw_data.get('author'),
            raw_data=raw_data,
            meta_info=news_data['meta_info']
        )

        self.db.add(news_item)
        self.db.flush()  # Get ID without committing
        return news_item

    async def _calculate_relevance_score(
        self, 
        news_item: Dict[str, Any], 
        transformed_content: str, 
        prompt: Prompt
    ) -> float:
        """
        Calculates relevance score for a news item relative to the prompt
        """
        # Implementation would depend on your scoring algorithm
        # This is a placeholder for the actual implementation
        return 0.5

    async def _process_metadata(
        self, 
        news_item: Dict[str, Any], 
        transformed: Any, 
        prompt: Prompt
    ) -> Dict[str, Any]:
        """
        Processes and enriches news metadata
        """
        # Implementation would depend on your metadata requirements
        # This is a placeholder for the actual implementation
        return {}

    def _get_last_refresh_time(self, prompt_id: int) -> Optional[datetime]:
        """
        Gets the last refresh time for a prompt
        """
        result = self.db.query(func.max(News.created_at)).join(
            news_prompts
        ).filter(
            news_prompts.c.prompt_id == prompt_id
        ).scalar()
        return result

    def _get_existing_news_for_prompt(self, prompt_id: int) -> List[News]:
        """
        Retrieves existing news for a prompt
        """
        return self.db.query(News).join(
            news_prompts
        ).filter(
            news_prompts.c.prompt_id == prompt_id
        ).order_by(
            news_prompts.c.display_order
        ).all()
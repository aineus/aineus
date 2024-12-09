from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging
from newsapi import NewsApiClient
from app.models.news import News, Category, NewsTransformation, news_prompts
from app.models.prompt import Prompt
from app.core.llm.factory import LLMFactory
from app.core.config import get_settings
from sqlalchemy import and_, or_, func

logger = logging.getLogger(__name__)
settings = get_settings()

class NewsCollector:
    def __init__(self, db: Session):
        self.db = db
        self.llm_factory = LLMFactory()
        self.newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

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
        # Get preferences from prompt
        preferences = prompt.source_preferences or {}
        categories = prompt.custom_categories or {}
        
        # Default query parameters
        query_params = {
            'language': preferences.get('language', 'en'),
            'sortBy': preferences.get('sort_by', 'relevancy'),
            'pageSize': prompt.max_articles or 100,
            'from': (datetime.utcnow() - timedelta(days=1)).isoformat()
        }
        
        # Add category if specified
        if categories.get('newsapi_category'):
            query_params['category'] = categories['newsapi_category']
        
        # Add sources if specified
        if preferences.get('sources'):
            query_params['sources'] = ','.join(preferences['sources'])
        
        # Add search query if specified
        if preferences.get('keywords'):
            query_params['q'] = ' OR '.join(preferences['keywords'])
        
        try:
            response = self.newsapi.get_everything(**query_params)
            
            # Transform to our standard format
            news_items = []
            for article in response['articles']:
                news_items.append({
                    'title': article['title'],
                    'content': article['content'] or article['description'],
                    'summary': article['description'],
                    'source': article['source']['name'],
                    'url': article['url'],
                    'published_at': datetime.strptime(
                        article['publishedAt'], 
                        '%Y-%m-%dT%H:%M:%SZ'
                    ),
                    'image_url': article['urlToImage'],
                    'author': article['author'],
                    'raw_data': article
                })
            
            return news_items
            
        except Exception as e:
            logger.error(f"Error collecting news: {str(e)}")
            return []

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

        # Sort by relevance score
        processed_news.sort(key=lambda x: x['relevance_score'], reverse=True)
        return processed_news

    async def _calculate_relevance_score(
        self, 
        news_item: Dict[str, Any], 
        transformed_content: str, 
        prompt: Prompt
    ) -> float:
        """
        Calculates relevance score for a news item relative to the prompt
        """
        try:
            # Use LLM to calculate relevance
            llm = self.llm_factory.create(provider=prompt.llm_provider)
            
            relevance_prompt = f"""
            On a scale of 0 to 1, how relevant is this news article to the following criteria?
            Consider factors like:
            - Timeliness
            - Impact
            - Relevance to topics: {prompt.source_preferences.get('keywords', [])}
            - Quality of information
            
            Article: {news_item['title']}
            {news_item['content'][:500]}...  # Truncate for token limits
            
            Return only the number between 0 and 1.
            """
            
            response = await llm.generate(prompt=relevance_prompt)
            try:
                score = float(response.content.strip())
                return max(0.0, min(1.0, score))  # Ensure between 0 and 1
            except ValueError:
                return 0.5  # Default if unable to parse
                
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
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
        try:
            # Extract reading time
            word_count = len(news_item['content'].split())
            reading_time = round(word_count / 200)  # Assuming 200 words per minute
            
            # Basic sentiment analysis (can be enhanced with NLP)
            sentiment_prompt = f"""
            Analyze the sentiment of this text. Return only a number:
            -1 for negative
            0 for neutral
            1 for positive

            Text: {news_item['title']} {news_item['content'][:200]}
            """
            
            llm = self.llm_factory.create(provider=prompt.llm_provider)
            sentiment_response = await llm.generate(prompt=sentiment_prompt)
            try:
                sentiment_score = float(sentiment_response.content.strip())
            except ValueError:
                sentiment_score = 0
                
            return {
                "reading_time": reading_time,
                "word_count": word_count,
                "sentiment_score": sentiment_score,
                "processed_at": datetime.utcnow().isoformat(),
                "source_metadata": news_item['raw_data'].get('metadata', {}),
                "llm_metadata": transformed.meta_info
            }
            
        except Exception as e:
            logger.error(f"Error processing metadata: {e}")
            return {}

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
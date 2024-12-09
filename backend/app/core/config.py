from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, List

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "MyNeos"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # openai, llama, mistral
    OPENAI_API_KEY: Optional[str] = None
    LOCAL_LLM_URL: Optional[str] = None
    LOCAL_LLM_MODEL: Optional[str] = None
    
    # News API
    NEWS_API_KEY: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    # News Collection
    NEWS_UPDATE_INTERVAL: int = 30  # minutes
    NEWS_SOURCES: List[str] = ["newsapi", "reuters"]
    
    class Config:
        env_file = ".env"

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

@lru_cache()
def get_settings():
    return Settings()
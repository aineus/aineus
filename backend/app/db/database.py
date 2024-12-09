from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# Log the connection URL (without password)
connection_url = settings.sqlalchemy_database_url
safe_url = connection_url.replace(settings.POSTGRES_PASSWORD, "***") if settings.POSTGRES_PASSWORD else connection_url
logger.info(f"Connecting to database: {safe_url}")

engine = create_engine(
    settings.sqlalchemy_database_url,
    echo=True  # This will log all SQL statements
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
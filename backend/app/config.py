from pydantic_settings import BaseSettings
from typing import ClassVar, List, Optional
from pydantic import field_validator
import os
from dotenv import load_dotenv

# Load environment variables before settings initialization
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "News Chatbot"
    DEBUG: bool = False
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_DB: int = 0
    SESSION_TTL: int = 86400  # 24 hours in seconds
    CHROMA_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "news_articles"
    
    EMBEDDING_MODEL: ClassVar[str] = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000  # Size of text chunks for embedding
    CHUNK_OVERLAP: int = 200  # Overlap between chunks
    
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    
    NEWS_SOURCES: List[str] = [
    "https://www.aljazeera.com/xml/rss/all.xml",
]
    
    REQUEST_TIMEOUT: int = 10  # seconds
    MAX_ARTICLES_PER_SOURCE: int = 50
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    @field_validator('GEMINI_API_KEY', mode='before')
    def validate_gemini_key(cls, v):
        if v is None:
            print("Warning: GEMINI_API_KEY not set. Some features may not work.")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Initialize settings with fallback
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Continuing with default settings...")
    settings = Settings(GEMINI_API_KEY=None)  # Fallback initialization
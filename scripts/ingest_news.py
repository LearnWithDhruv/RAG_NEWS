import sys
import os
import redis
import traceback
from typing import List, Dict, Any
from dotenv import load_dotenv

# Calculate project root (parent of 'scripts' directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Debug: Log sys.path to verify module search paths
print(f"DEBUG: sys.path: {sys.path}")

# Import logger first
from backend.app.utils.logger import logger

# Load environment variables from project root
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)
logger.info(f"Loaded .env from: {env_path}")

from backend.app.services.news_service import NewsService
from backend.app.database.chroma_client import chroma_client
from backend.app.services.embedding_service import get_embeddings
from backend.app.config import settings

def validate_article(article: Dict[str, Any]) -> bool:
    """Enhanced article validation with debug logging"""
    required_fields = ['title', 'url', 'chunks']
    missing_fields = [field for field in required_fields if field not in article or not article[field]]
    
    if missing_fields:
        logger.error(f"Article missing fields {missing_fields}: {article}")
        return False
        
    if not isinstance(article['chunks'], list):
        logger.error(f"Invalid chunks type for article: {article}")
        return False
        
    if not article['chunks']:
        logger.warning(f"No chunks in article: {article}")
        return False
        
    logger.debug(f"Validated article: {article['title']}")
    return True

def initialize_services():
    """Initialize all required services with robust error handling"""
    try:
        logger.info("Initializing Redis client...")
        redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            socket_timeout=10,
            socket_connect_timeout=5
        )
        redis_client.ping()
        logger.info("Redis initialized successfully")

        logger.info("Initializing ChromaDB collection...")
        try:
            chroma_client.delete_collection(name=settings.COLLECTION_NAME)
            logger.info(f"Deleted ChromaDB collection '{settings.COLLECTION_NAME}'")
        except Exception as e:
            if "Collection not found" in str(e):
                logger.info(f"Collection '{settings.COLLECTION_NAME}' not found, will create a new one")
            else:
                logger.warning(f"Error deleting collection: {e}")

        collection = chroma_client.create_collection(name=settings.COLLECTION_NAME)
        logger.info(f"Created new ChromaDB collection '{settings.COLLECTION_NAME}'")

        # Verify collection creation
        collection_count = collection.count()
        logger.info(f"Initial collection count: {collection_count}")

        return redis_client, collection

    except Exception as e:
        logger.error(f"Service initialization failed: {e}")
        logger.error(traceback.format_exc())
        raise

def process_chunk(chunk: str, article: Dict[str, Any], collection: Any, chunk_idx: int, article_idx: int) -> bool:
    """Process a single chunk with comprehensive error handling"""
    try:
        if not chunk.strip():
            logger.debug(f"Skipping empty chunk {chunk_idx} for article {article['title']}")
            return False

        embedding = get_embeddings(chunk)
        if embedding is None:
            logger.error(f"Embedding failed for chunk {chunk_idx} in article {article['title']}")
            return False

        chunk_id = f"{article['url']}-{chunk_idx}"
        collection.add(
            embeddings=[embedding.tolist()],
            documents=[chunk],
            metadatas=[{
                "title": article['title'],
                "url": article['url'],
                "published_date": article.get('published_date', ''),
                "chunk_index": chunk_idx,
                "article_index": article_idx
            }],
            ids=[chunk_id]
        )
        logger.debug(f"Stored chunk {chunk_idx} for article {article_idx}: {article['title']}")
        return True

    except Exception as e:
        logger.error(f"Chunk processing error for chunk {chunk_idx} in article {article['title']}: {e}")
        logger.debug(traceback.format_exc())
        return False

def process_article(article: Dict[str, Any], redis_client: redis.Redis, collection: Any, idx: int) -> int:
    """Process a single article end-to-end"""
    if not validate_article(article):
        logger.warning(f"Skipping article {idx} due to validation failure: {article.get('title', 'Untitled')}")
        return 0

    try:
        # Store metadata in Redis
        redis_key = f"article:{idx}"
        redis_client.hset(redis_key, mapping={
            "title": article["title"],
            "url": article["url"],
            "published_date": article.get("published_date", ""),
            "source": article.get("source", "unknown"),
            "chunk_count": str(len(article['chunks']))
        })
        logger.debug(f"Stored article metadata in Redis: {redis_key}")

        # Process chunks and store in ChromaDB
        successful_chunks = 0
        for i, chunk in enumerate(article['chunks']):
            if process_chunk(chunk, article, collection, i, idx):
                successful_chunks += 1
            else:
                logger.warning(f"Failed to process chunk {i} for article {idx}: {article['title']}")

        if successful_chunks == 0:
            logger.warning(f"No chunks successfully processed for article {idx}: {article['title']}")
        else:
            logger.info(f"Processed {successful_chunks}/{len(article['chunks'])} chunks for article {idx}: {article['title']}")
        return successful_chunks

    except Exception as e:
        logger.error(f"Article processing failed for article {idx}: {article.get('title', 'Untitled')}: {e}")
        logger.error(traceback.format_exc())
        return 0

def main():
    try:
        logger.info("Starting news ingestion")
        
        # Initialize services
        redis_client, collection = initialize_services()
        
        # Fetch articles
        news_service = NewsService()
        articles = news_service.fetch_articles(limit=50)
        logger.info(f"Fetched {len(articles)} articles")
        
        if not articles:
            logger.warning("No articles fetched. Exiting ingestion.")
            return 1

        # Clear existing Redis data
        redis_client.flushdb()
        logger.info("Cleared Redis database")
        
        # Process all articles
        total_chunks = 0
        successful_articles = 0
        
        for idx, article in enumerate(articles):
            logger.info(f"\n=== Processing article {idx + 1}/{len(articles)} ===")
            logger.info(f"Title: {article['title'][:50]}...")
            
            chunks_processed = process_article(article, redis_client, collection, idx)
            if chunks_processed > 0:
                total_chunks += chunks_processed
                successful_articles += 1

        # Verify ChromaDB storage
        collection_count = collection.count()
        logger.info(f"Final ChromaDB collection count: {collection_count}")

        # Final report
        stored_articles = redis_client.keys('article:*')
        logger.info("\n=== INGESTION COMPLETE ===")
        logger.info(f"Total articles fetched: {len(articles)}")
        logger.info(f"Successfully processed: {successful_articles}")
        logger.info(f"Total chunks stored in ChromaDB: {total_chunks}")
        
        # Verify storage in Redis
        if stored_articles:
            logger.info(f"\nFirst 3 articles in Redis:")
            for key in stored_articles[:3]:
                data = {k.decode(): v.decode() for k, v in redis_client.hgetall(key).items()}
                logger.info(f"{key.decode()}: {data}")
        else:
            logger.warning("No articles found in Redis after ingestion.")

        return 0

    except Exception as e:
        logger.error(f"Fatal error in ingestion: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
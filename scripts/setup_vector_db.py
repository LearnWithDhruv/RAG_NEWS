import sys
import os
import traceback
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from correct path
env_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', '.env')
load_dotenv(env_path)

# Verify environment loading
print(f"Loading .env from: {env_path}")
print(f"GEMINI_API_KEY present: {'GEMINI_API_KEY' in os.environ}")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.database.chroma_client import chroma_client
from backend.app.config import settings
from backend.app.utils.logger import logger

def setup_collection(collection_name: str) -> bool:
    """Initialize or reset the ChromaDB collection"""
    try:
        # Delete collection if exists
        try:
            chroma_client.delete_collection(name=collection_name)
            logger.info(f"Deleted existing collection '{collection_name}'")
        except Exception as e:
            if "Collection not found" not in str(e):
                logger.warning(f"Delete error: {e}")
            else:
                logger.info("No existing collection to delete")
        
        # Create new collection
        chroma_client.create_collection(name=collection_name)
        logger.info(f"Created collection '{collection_name}'")
        return True
    except Exception as e:
        logger.error(f"Setup error: {e}")
        return False

def main():
    logger.info("Starting vector database setup")
    
    try:
        if setup_collection(settings.COLLECTION_NAME):
            logger.info("Vector database setup completed successfully")
            return 0
        else:
            logger.error("Vector database setup failed")
            return 1
    except Exception as e:
        logger.error(f"Error in vector database setup: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
import chromadb
import os
from backend.app.utils.logger import logger

# Configure ChromaDB with persistence
try:
    # Ensure the path is absolute and points to scripts/chroma_db
    chroma_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'chroma_db'))
    # Create the directory if it doesn't exist
    os.makedirs(chroma_db_path, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    logger.info(f"ChromaDB client initialized successfully with persistence path: {chroma_db_path}")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB client: {e}")
    raise
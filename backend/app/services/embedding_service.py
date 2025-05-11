from sentence_transformers import SentenceTransformer
from backend.app.utils.logger import logger

class EmbeddingService:
    def __init__(self):
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded embedding model: all-MiniLM-L6-v2")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def get_embeddings(self, text: str):
        try:
            if not text or not isinstance(text, str):
                logger.warning(f"Invalid text for embedding: {text}")
                return None
            embedding = self.model.encode(text, convert_to_numpy=True)
            if embedding is None or len(embedding) == 0:
                logger.error(f"Embedding generation returned empty result for text: {text[:50]}...")
                return None
            return embedding
        except Exception as e:
            logger.error(f"Embedding generation failed for text: {text[:50]}...: {e}")
            return None

embedding_service = EmbeddingService()

def get_embeddings(text: str):
    return embedding_service.get_embeddings(text)
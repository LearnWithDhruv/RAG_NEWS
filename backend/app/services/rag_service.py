from typing import List, Optional
from backend.app.database.chroma_client import chroma_client
from backend.app.services.embedding_service import get_embeddings
from backend.app.utils.logger import logger
from backend.app.config import settings

class RAGService:
    def __init__(self):
        try:
            self.collection = chroma_client.get_collection(name=settings.COLLECTION_NAME)
            logger.info("RAGService initialized with ChromaDB collection")
        except Exception as e:
            logger.error(f"Failed to initialize RAGService: {e}")
            raise

    def retrieve_context(self, query: str, top_k: int = 3) -> Optional[List[str]]:
        """Retrieve relevant context for a query using ChromaDB"""
        try:
            if not query.strip():
                logger.warning("Empty query provided for context retrieval")
                return None

            # Generate embedding for the query
            logger.debug(f"Generating embedding for query: {query}")
            query_embedding = get_embeddings(query)
            if query_embedding is None:
                logger.error("Failed to generate embedding for query")
                return None

            # Query ChromaDB for similar documents
            logger.debug(f"Querying ChromaDB with top_k={top_k}")
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )

            # Extract documents from results
            if not results or not results.get("documents"):
                logger.warning("No documents found in ChromaDB for the query")
                return None

            documents = results["documents"][0]
            logger.debug(f"Retrieved {len(documents)} documents from ChromaDB")
            return documents

        except Exception as e:
            logger.error(f"Error retrieving context from ChromaDB: {e}")
            return None
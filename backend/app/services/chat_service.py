# backend/app/services/chat_service.py
from typing import List, Dict
from app.database.chroma_client import chroma_client
from app.services.embedding_service import get_embeddings
import redis
import json

class ChatService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.collection = chroma_client.get_collection("news_articles")
    
    async def search_news(self, query: str) -> List[Dict]:
        """Search news articles using vector similarity"""
        query_embedding = get_embeddings(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=10
        )
        
        articles = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            articles.append({
                "title": metadata['title'],
                "url": metadata['url'],
                "snippet": doc[:200] + "...",
                "published_date": metadata.get('published_date', '')
            })
        
        return articles
    
    async def get_chat_response(self, query: str) -> Dict:
        """Get a chat response using RAG with news context"""
        # First get relevant news context
        query_embedding = get_embeddings(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=5
        )
        
        # Build context from top results
        context = "\n\n".join([
            f"Article: {results['metadatas'][0][i]['title']}\n"
            f"Content: {doc}\n"
            f"Source: {results['metadatas'][0][i]['url']}"
            for i, doc in enumerate(results['documents'][0])
        ])
        
        # Get response from LLM (Gemini in your case)
        prompt = f"""
        You are a news assistant. Answer the user's question using only the provided context.
        If you don't know the answer, say you don't know based on current news.
        
        Question: {query}
        
        Context:
        {context}
        """
        
        # This would use your Gemini integration
        response = await self._get_llm_response(prompt)
        
        return {
            "answer": response,
            "sources": [
                {"title": results['metadatas'][0][i]['title'], 
                 "url": results['metadatas'][0][i]['url']}
                for i in range(len(results['documents'][0]))
            ]
        }
    
    async def get_recent_news(self) -> List[Dict]:
        """Get recently ingested news from Redis"""
        articles = []
        for key in self.redis_client.keys('article:*'):
            data = self.redis_client.hgetall(key)
            articles.append({
                "title": data[b'title'].decode(),
                "url": data[b'url'].decode(),
                "snippet": f"Recent news about {data[b'title'].decode()[:50]}...",
                "published_date": data[b'published_date'].decode()
            })
        return articles[:10]  # Return top 10 recent
    
    async def _get_llm_response(self, prompt: str) -> str:
        """Implement your Gemini API call here"""
        # Your existing Gemini integration code goes here
        return "Sample response based on news context..."
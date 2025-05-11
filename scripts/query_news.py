import sys
import os
import asyncio
from typing import Optional
from dotenv import load_dotenv

# Set up paths and environment
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

from backend.app.services.rag_service import RAGService
from backend.app.services.gemini_service import generate_response
from backend.app.utils.logger import logger
from backend.app.database.redis_client import redis_client

class NewsQueryInterface:
    def __init__(self):
        self.rag_service = RAGService()
        self.session_id = "terminal-session"
        self.chat_history = []
        self.max_history_display = 5  # Limit displayed history entries
        
    async def get_context(self, query: str) -> Optional[str]:
        """Retrieve relevant context for a query"""
        try:
            contexts = self.rag_service.retrieve_context(query, top_k=3)
            if not contexts:
                logger.warning("No relevant context found for the query in ChromaDB")
                return None
            return "\n\n---\n\n".join(contexts)
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return None
    
    async def ask_question(self, question: str) -> str:
        """Process a question through the RAG pipeline"""
        if not question.strip():
            return "Please enter a valid question."
            
        logger.info(f"Processing question: {question}")
        
        # Get relevant context
        context = await self.get_context(question)
        if not context:
            return "I couldn't find any relevant news articles in the database to answer your question. Please ensure articles have been ingested using ingest_news.py."
        
        # Generate response using Gemini with a timeout
        try:
            response = await asyncio.wait_for(generate_response(question, context), timeout=30.0)
            self.chat_history.append({"question": question, "response": response})
            return response
        except asyncio.TimeoutError:
            logger.error("Gemini API call timed out after 30 seconds")
            return "Sorry, the response generation timed out. Please try again later."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while generating a response."

    def display_history(self):
        """Display recent chat history"""
        if not self.chat_history:
            print("No chat history available.")
            return

        print("\n=== Recent Chat History ===")
        start_idx = max(0, len(self.chat_history) - self.max_history_display)
        for idx, entry in enumerate(self.chat_history[start_idx:], start=start_idx + 1):
            print(f"\nQ{idx}: {entry['question']}")
            print(f"A{idx}: {entry['response']}")

async def main():
    print("\n=== News Chatbot Terminal Interface ===")
    print("Commands:")
    print("- Type 'exit' or 'quit' to end the session")
    print("- Type 'history' to view recent chat history")
    print("- Ask any question about the news to get a response\n")
    
    interface = NewsQueryInterface()
    
    while True:
        try:
            question = input("\nYour question about the news: ").strip()
            
            if question.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
                
            if question.lower() == 'history':
                interface.display_history()
                continue
                
            if not question:
                print("Please enter a question.")
                continue
                
            response = await interface.ask_question(question)
            print("\nResponse:")
            print(response)
            
        except KeyboardInterrupt:
            print("\nSession ended by user.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
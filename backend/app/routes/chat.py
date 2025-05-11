from fastapi import APIRouter, HTTPException
from backend.app.services.rag_service import RAGService
from backend.app.database.redis_client import redis_client
from backend.app.utils.logger import logger
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    sessionId: str
    message: str

@router.post("/")
async def chat_with_bot(request: ChatRequest):
    try:
        # Get session messages from Redis
        session_key = f"session:{request.sessionId}"
        messages = await redis_client.lrange(session_key, 0, -1)
        
        # Process with RAG
        rag_service = RAGService()
        response = await rag_service.generate_response(
            request.message,
            session_id=request.sessionId,
            chat_history=messages
        )
        
        # Store both messages in Redis
        await redis_client.rpush(session_key, f"user:{request.message}")
        await redis_client.rpush(session_key, f"assistant:{response}")
        
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing chat request")
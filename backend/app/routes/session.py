from fastapi import APIRouter, HTTPException
from backend.app.database.redis_client import redis_client
from backend.app.utils.logger import logger
import uuid

router = APIRouter()

@router.post("/session")
async def create_session():
    try:
        session_id = str(uuid.uuid4())
        session_key = f"session:{session_id}"
        await redis_client.set(session_key, "")
        return {"sessionId": session_id, "messages": []}
    except Exception as e:
        logger.error(f"Session creation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating session")

@router.delete("/session/{session_id}")
async def reset_session(session_id: str):
    try:
        session_key = f"session:{session_id}"
        await redis_client.delete(session_key)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Session reset error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error resetting session")
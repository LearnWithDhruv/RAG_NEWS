from pydantic import BaseModel, UUID4, Field
from typing import Optional

class ChatRequest(BaseModel):
    """Request model for chat messages"""
    session_id: UUID4
    message: str = Field(..., min_length=1, max_length=1000)

class ChatResponse(BaseModel):
    """Response model for chat messages"""
    message: str
    session_id: UUID4
from pydantic import BaseModel, UUID4
from typing import Optional

class SessionCreate(BaseModel):
    """Request model for creating a session"""
    pass

class SessionResponse(BaseModel):
    """Response model for session operations"""
    id: UUID4
    status: str
    message: Optional[str] = None
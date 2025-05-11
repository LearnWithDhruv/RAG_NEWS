from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import chat, news
from backend.app.config import settings
from backend.app.utils.logger import logger
import uvicorn

app = FastAPI(
    title="News Chatbot API",
    description="RAG-powered chatbot for news websites",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(news.router, prefix="/api/v1/news", tags=["news"])

@app.get("/")
def health_check():
    logger.info("Health check endpoint hit")
    return {"status": "healthy", "app": settings.APP_NAME}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
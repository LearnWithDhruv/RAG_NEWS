import json
import redis
import uuid
from backend.app.config import settings
from backend.app.utils.logger import logger

class RedisClient:
    def __init__(self):
        try:
            self.client = redis.Redis.from_url(settings.REDIS_URL)
            self.client.ping()  # Test connection
            self.ttl = settings.SESSION_TTL
            logger.info("Redis client initialized successfully")
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            raise

    def create_session(self) -> str:
        """Create a new session with empty messages"""
        session_id = str(uuid.uuid4())
        initial_data = {"messages": []}
        self.client.setex(
            f"session:{session_id}",
            self.ttl,
            json.dumps(initial_data)
        )
        return session_id

    def get_session(self, session_id: str) -> dict:
        """Retrieve session data"""
        data = self.client.get(f"session:{session_id}")
        return json.loads(data) if data else None

    def update_session(self, session_id: str, messages: list) -> bool:
        """Update session messages"""
        current_data = self.get_session(session_id)
        if not current_data:
            return False
            
        current_data["messages"] = messages
        return bool(
            self.client.setex(
                f"session:{session_id}",
                self.ttl,
                json.dumps(current_data)
            )
        )

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        return bool(self.client.delete(f"session:{session_id}"))

    def get(self, key: str) -> bytes:
        """Retrieve a value by key"""
        try:
            return self.client.get(key)
        except redis.RedisError as e:
            logger.error(f"Redis get error for key {key}: {e}")
            raise

    def setex(self, key: str, ttl: int, value: str) -> bool:
        """Set a value with an expiration time"""
        try:
            return bool(self.client.setex(key, ttl, value))
        except redis.RedisError as e:
            logger.error(f"Redis setex error for key {key}: {e}")
            raise

redis_client = RedisClient()
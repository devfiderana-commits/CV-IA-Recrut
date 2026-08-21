"""
Placeholder database module.
MongoDB will be configured in a later phase.
"""
from typing import Any, Optional
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings

_client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo() -> None:
    global _client
    if not settings.mongodb_uri:
        logging.info("No MongoDB URI provided; skipping DB connection.")
        return

    try:
        _client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
        # verify connection
        await _client.admin.command("ping")
        logging.info("Connected to MongoDB")
    except Exception as exc:
        _client = None
        logging.error("Could not connect to MongoDB: %s", exc)
        raise


def get_db() -> Any:
    if _client is None:
        raise RuntimeError("Database not configured or not connected. Set `MONGODB_URI` in .env to connect.")
    return _client[settings.database_name]


def close_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


async def is_connected() -> bool:
    """Return True if MongoDB client is connected and responds to ping."""
    if _client is None:
        return False
    try:
        await _client.admin.command("ping")
        return True
    except Exception:
        return False

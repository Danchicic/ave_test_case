import logging
import os

from redis.asyncio import Redis

logger = logging.getLogger(__name__)
try:
    __redis_client = Redis(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        db=os.environ.get("REDIS_DB"),
    )
    logger.info("Успешное подключение к Redis")
except Exception:
    logger.exception(f"Ошибка подключения к Redis")
    raise


def get_redis():
    return __redis_client


def get_phone_key(phone: str) -> str:
    return f"phone:{phone}"

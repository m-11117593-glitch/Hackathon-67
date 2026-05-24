import asyncio
import logging
import random
from functools import wraps

logger = logging.getLogger(__name__)


def async_retry(max_retries=2, delay=1.5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)

                except Exception as e:
                    last_exception = e
                    wait = delay * (attempt + 1) + random.uniform(0, 0.5)

                    logger.warning(
                        f"[Retry {attempt + 1}/{max_retries + 1}] {func.__name__} failed: {e}"
                    )

                    await asyncio.sleep(wait)

            # 🔥 IMPORTANT CHANGE: do NOT crash pipeline
            logger.error(
                f"FAILED permanently after {max_retries + 1} attempts: {func.__name__} -> {last_exception}"
            )

            return None   # instead of raising

        return wrapper
    return decorator
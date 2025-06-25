import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=1)

logger = logging.getLogger(__name__)

async def run_blocking(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    logger.debug(f"Call of blocking function: {func.__name__} with args={args} kwargs={kwargs}")
    return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))

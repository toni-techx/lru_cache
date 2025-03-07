import time

from fastapi import Request

from app.core import logger


async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url} processed in {process_time:.4f} seconds")
    return response

"""FastAPI application entrypoint."""

import logging
import time
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import get_settings
from src.errors import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from src.logging_config import configure_logging
from src.middleware import RateLimitMiddleware
from src.routes.tasks import router as tasks_router

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description=(
        "A small RESTful Task Manager service with in-memory storage, "
        "standard JSON responses, logging, validation, Swagger documentation, "
        "container support, Kubernetes manifests, and CI/CD configuration."
    ),
)

app.add_middleware(RateLimitMiddleware, limit=settings.rate_limit_per_minute)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.include_router(tasks_router)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    """Log request method, path, response status, and latency."""
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s -> %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/health", tags=["health"], summary="Health check")
def health_check() -> dict[str, str]:
    """Return service health information for Docker and Kubernetes probes."""
    return {
        "status": "ok",
        "service": settings.service_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

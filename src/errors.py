"""Centralized JSON error response handlers."""

import logging
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def error_payload(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    """Build a consistent error response body."""
    payload: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    return payload


async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Convert HTTP errors into the standard JSON error format."""
    status_code = exc.status_code
    code = "not_found" if status_code == 404 else "http_error"
    message = str(exc.detail) if exc.detail else "HTTP error"
    return JSONResponse(status_code=status_code, content=error_payload(code, message))


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return validation failures as HTTP 400 for homework compatibility."""
    return JSONResponse(
        status_code=400,
        content=error_payload("validation_error", "Invalid request payload", exc.errors()),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Log unexpected exceptions and hide internals from API clients."""
    logger.exception(
        "Unhandled exception for %s %s", request.method, request.url.path, exc_info=exc
    )
    return JSONResponse(
        status_code=500,
        content=error_payload("internal_server_error", "Internal server error"),
    )

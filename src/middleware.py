"""Custom ASGI middleware."""

from collections import defaultdict, deque
import time
from typing import Deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.errors import error_payload


class RateLimitMiddleware(BaseHTTPMiddleware):
    """A lightweight per-client sliding-window request limiter."""

    def __init__(
        self, app, limit: int = 100, window_seconds: int = 60
    ) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.limit = max(limit, 1)
        self.window_seconds = window_seconds
        self.requests: dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(
        self, request: Request, call_next
    ) -> Response:  # type: ignore[no-untyped-def]
        client_host = request.client.host if request.client else "anonymous"
        key = f"{client_host}:{request.url.path}"
        now = time.monotonic()
        timestamps = self.requests[key]

        while timestamps and now - timestamps[0] > self.window_seconds:
            timestamps.popleft()

        if len(timestamps) >= self.limit:
            return JSONResponse(
                status_code=429,
                content=error_payload("rate_limited", "Too many requests"),
                headers={
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        timestamps.append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(max(self.limit - len(timestamps), 0))
        return response

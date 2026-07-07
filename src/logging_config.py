"""Logging setup for the API service."""

import logging


def configure_logging(log_level: str) -> None:
    """Configure root logging with a compact production-friendly format."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

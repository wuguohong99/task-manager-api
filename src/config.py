"""Application configuration helpers."""

from dataclasses import dataclass
import os


def _positive_int_from_env(name: str, default: int) -> int:
    """Return a positive integer from an environment variable."""
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        value = int(raw_value)
    except ValueError:
        return default
    return value if value > 0 else default


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    service_name: str = os.getenv("SERVICE_NAME", "task-manager-api")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    rate_limit_per_minute: int = _positive_int_from_env("RATE_LIMIT_PER_MINUTE", 100)


def get_settings() -> Settings:
    """Create a Settings instance."""
    return Settings()

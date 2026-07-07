"""Task domain models used by the REST API."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    """Allowed task workflow statuses."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class TaskCreate(BaseModel):
    """Payload required to create a task."""

    title: str = Field(..., min_length=1, max_length=120, examples=["Write README"])
    description: str = Field(default="", max_length=500, examples=["Document local run steps"])
    status: TaskStatus = Field(default=TaskStatus.TODO, examples=["todo"])


class TaskUpdate(BaseModel):
    """Payload accepted for partial task updates."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[TaskStatus] = None


class Task(BaseModel):
    """Task resource returned by the API."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "2f0f7baf-2c26-4a97-9a2e-c5b2dd23e9c3",
                "title": "Write README",
                "description": "Document local run steps",
                "status": "todo",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            }
        }
    )

    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

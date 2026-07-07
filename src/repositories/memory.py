"""Thread-safe in-memory task repository.

The homework explicitly allows in-memory storage. This repository hides storage
behind a small interface so it can be replaced by a database implementation
later without changing route handlers.
"""

from threading import Lock
from uuid import UUID

from src.models.task import Task, TaskCreate, TaskUpdate, utc_now


class MemoryTaskStore:
    """A simple thread-safe in-memory task store."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}
        self._lock = Lock()

    def list_tasks(self) -> list[Task]:
        """Return all tasks ordered by creation time."""
        with self._lock:
            tasks = [task.model_copy(deep=True) for task in self._tasks.values()]
        return sorted(tasks, key=lambda task: task.created_at)

    def get_task(self, task_id: UUID) -> Task | None:
        """Return one task by ID or None when it does not exist."""
        with self._lock:
            task = self._tasks.get(task_id)
            return task.model_copy(deep=True) if task else None

    def create_task(self, payload: TaskCreate) -> Task:
        """Create and persist a new task."""
        task = Task(**payload.model_dump())
        with self._lock:
            self._tasks[task.id] = task
        return task.model_copy(deep=True)

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> Task | None:
        """Update an existing task and return it, or None if it is missing."""
        with self._lock:
            existing = self._tasks.get(task_id)
            if existing is None:
                return None

            changes = payload.model_dump(exclude_unset=True)
            updated = existing.model_copy(update={**changes, "updated_at": utc_now()})
            self._tasks[task_id] = updated
            return updated.model_copy(deep=True)

    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task by ID. Returns True when a task was deleted."""
        with self._lock:
            if task_id not in self._tasks:
                return False
            del self._tasks[task_id]
            return True

    def clear(self) -> None:
        """Remove all tasks. Used by tests."""
        with self._lock:
            self._tasks.clear()


task_store = MemoryTaskStore()

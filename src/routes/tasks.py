"""Task CRUD route handlers."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from src.models.task import Task, TaskCreate, TaskUpdate
from src.repositories.memory import task_store

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=list[Task], summary="List all tasks")
def list_tasks() -> list[Task]:
    """Return every task in the in-memory store."""
    return task_store.list_tasks()


@router.get("/tasks/{task_id}", response_model=Task, summary="Get one task")
def get_task(task_id: UUID) -> Task:
    """Return a single task by UUID."""
    task = task_store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
def create_task(payload: TaskCreate) -> Task:
    """Create a new task."""
    return task_store.create_task(payload)


@router.put("/tasks/{task_id}", response_model=Task, summary="Update a task")
def update_task(task_id: UUID, payload: TaskUpdate) -> Task:
    """Update an existing task."""
    task = task_store.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: UUID) -> Response:
    """Delete a task by UUID."""
    deleted = task_store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

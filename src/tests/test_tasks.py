"""API tests for the Task Manager service."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.repositories.memory import task_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store() -> None:
    """Ensure each test starts from an empty task store."""
    task_store.clear()
    yield
    task_store.clear()


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "task-manager-api"


def test_create_and_list_tasks() -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover the task CRUD endpoints",
            "status": "todo",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "Write tests"
    assert created_task["status"] == "todo"
    assert "id" in created_task

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert list_response.json() == [created_task]


def test_get_task_by_id() -> None:
    created_task = client.post("/tasks", json={"title": "Read docs"}).json()

    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]


def test_get_missing_task_returns_404() -> None:
    response = client.get(f"/tasks/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_update_task() -> None:
    created_task = client.post("/tasks", json={"title": "Draft README"}).json()

    response = client.put(
        f"/tasks/{created_task['id']}",
        json={"title": "Finish README", "status": "done"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Finish README"
    assert body["status"] == "done"
    assert body["updated_at"] != created_task["updated_at"]


def test_update_missing_task_returns_404() -> None:
    response = client.put(f"/tasks/{uuid4()}", json={"title": "Missing"})

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Task not found"


def test_delete_task() -> None:
    created_task = client.post("/tasks", json={"title": "Delete me"}).json()

    delete_response = client.delete(f"/tasks/{created_task['id']}")
    get_response = client.get(f"/tasks/{created_task['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_invalid_task_payload_returns_400() -> None:
    response = client.post("/tasks", json={"title": "", "status": "invalid"})

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"

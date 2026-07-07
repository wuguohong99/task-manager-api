# Task Manager API

[![CI](https://github.com/<your-username>/task-manager-api/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/task-manager-api/actions/workflows/ci.yml)

A RESTful Task Manager API built with Python 3.11 and FastAPI. The service supports task CRUD operations, health checks, in-memory storage, request validation, structured JSON errors, request logging, Swagger/OpenAPI documentation, unit tests, Docker containerization, Minikube Kubernetes deployment, and GitHub Actions CI/CD.

> Replace `<your-username>` in the CI badge after creating your GitHub repository.

## Tech stack

| Area | Technology |
| --- | --- |
| API framework | Python 3.11+, FastAPI, Pydantic |
| Server | Uvicorn |
| Tests | pytest, pytest-cov |
| Lint | pylint |
| Container | Docker, Docker Compose |
| Kubernetes | Minikube, kubectl, Ingress |
| CI/CD | GitHub Actions, Trivy, GHCR |

## Project structure

```text
task-manager-api/
├── .github/workflows/ci.yml
├── k8s/
│   ├── README.md
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── src/
│   ├── app.py
│   ├── config.py
│   ├── errors.py
│   ├── logging_config.py
│   ├── middleware.py
│   ├── models/task.py
│   ├── repositories/memory.py
│   ├── routes/tasks.py
│   └── tests/test_tasks.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── SUBMISSION_CHECKLIST.md
└── README.md
```

## API endpoints

| Method | Path | Description | Status codes |
| --- | --- | --- | --- |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get one task | 200 / 404 |
| POST | `/tasks` | Create a task | 201 / 400 |
| PUT | `/tasks/{id}` | Update a task | 200 / 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 / 404 |

Swagger UI is available at:

```bash
http://localhost:8080/docs
```

OpenAPI JSON is available at:

```bash
http://localhost:8080/openapi.json
```

## Task model

```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "status": "todo | in_progress | done",
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z"
}
```

## Local development

### 1. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 2. Run the API

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8080
```

### 3. Verify health

```bash
curl http://localhost:8080/health
```

Expected example:

```json
{
  "status": "ok",
  "service": "task-manager-api",
  "timestamp": "2026-01-01T00:00:00+00:00"
}
```

## API examples

### Create a task

```bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Write Kubernetes manifests","description":"Create namespace, deployment, service, configmap, ingress","status":"todo"}'
```

Expected status: `201 Created`.

### List tasks

```bash
curl http://localhost:8080/tasks
```

### Get one task

```bash
curl http://localhost:8080/tasks/<task-id>
```

### Update a task

```bash
curl -X PUT http://localhost:8080/tasks/<task-id> \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

### Delete a task

```bash
curl -X DELETE http://localhost:8080/tasks/<task-id>
```

Expected status: `204 No Content`.

## Run tests and coverage

```bash
pytest
```

The configured coverage gate is 60%:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=60
```

## Lint

```bash
pylint src --fail-under=8.0
```

## Runtime configuration

| Environment variable | Default | Description |
| --- | --- | --- |
| `SERVICE_NAME` | `task-manager-api` | Name returned by `/health` |
| `PORT` | `8080` | HTTP listen port used by Docker command |
| `HOST` | `0.0.0.0` | HTTP bind address used by Docker command |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `RATE_LIMIT_PER_MINUTE` | `100` | Sliding-window per-client per-path limit |

## Docker

### Build image

```bash
docker build -t task-manager-api .
```

### Run container

```bash
docker run --rm -p 8080:8080 task-manager-api
```

### Verify

```bash
curl http://localhost:8080/health
```

### Docker Compose

```bash
docker compose up --build
```

## Kubernetes with Minikube

See the detailed guide in [`k8s/README.md`](k8s/README.md).

Quick start:

```bash
minikube start
minikube addons enable ingress
docker build -t task-manager-api:latest .
minikube image load task-manager-api:latest
kubectl apply -f k8s/
kubectl rollout status deployment/task-manager-api -n task-manager
kubectl get all -n task-manager
```

Port-forward validation:

```bash
kubectl port-forward svc/task-manager-api -n task-manager 8080:8080
curl http://localhost:8080/health
curl http://localhost:8080/tasks
```

Ingress validation:

```bash
echo "$(minikube ip) task-manager.local" | sudo tee -a /etc/hosts
curl http://task-manager.local/health
curl http://task-manager.local/tasks
```

## CI/CD

The GitHub Actions workflow is defined in `.github/workflows/ci.yml` and runs on:

- Push to `main`
- Pull request to `main`

Pipeline stages:

1. Lint with `pylint`
2. Test with `pytest` and coverage threshold
3. Build Docker image
4. Scan the image with Trivy
5. Push image to GHCR on `main` branch pushes

The Docker image is tagged as:

```text
ghcr.io/<username>/task-manager-api:<sha>
```

## Git submission steps

If you use the provided zip that includes Git history, create an empty public GitHub repository named `task-manager-api`, then run:

```bash
cd task-manager-api
git remote add origin https://github.com/<your-username>/task-manager-api.git
git push -u origin main
git push origin feature/api feature/container-k8s feature/ci-docs v1.0.0
```

If you do not use the included Git history, create your own feature branches and Conventional Commits before submission.

Recommended final commit message:

```text
feat: complete homework submission
```

## Notes

- Storage is in memory as required by the homework, so tasks are reset when the process restarts.
- The repository does not contain secrets, tokens, passwords, or private keys.
- For screenshots, capture `kubectl get all -n task-manager` and successful API responses, then add them to the README if desired.

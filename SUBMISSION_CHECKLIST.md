# Homework Submission Checklist

Use this checklist before submitting the GitHub repository link.

## Task 1: Git and repository

- [ ] Repository is public and named `task-manager-api`.
- [ ] `README.md` exists and contains local, Docker, Kubernetes, and CI instructions.
- [ ] Branches exist: `main`, at least two `feature/*` branches.
- [ ] Commit messages follow Conventional Commits.
- [ ] Final commit message is `feat: complete homework submission`.
- [ ] `.gitignore` excludes virtual environments, IDE files, logs, and build artifacts.

## Task 2: REST API

- [x] `GET /health` returns HTTP 200.
- [x] `GET /tasks` returns all tasks.
- [x] `GET /tasks/{id}` returns HTTP 200 or 404.
- [x] `POST /tasks` returns HTTP 201 or 400.
- [x] `PUT /tasks/{id}` returns HTTP 200 or 404.
- [x] `DELETE /tasks/{id}` returns HTTP 204 or 404.
- [x] JSON data model includes `id`, `title`, `description`, `status`, `created_at`, `updated_at`.
- [x] Request validation, error handling, request logs, Swagger docs, tests, and rate limiting are included.

## Task 3: Docker

- [x] `Dockerfile` uses multi-stage build.
- [x] Runtime image uses an official `python:3.11-slim` base.
- [x] App runs as a non-root user.
- [x] Port can be configured with `PORT`, defaulting to 8080.
- [x] `.dockerignore` is included.
- [x] `docker-compose.yml` is included.

## Task 4: Kubernetes

- [x] Namespace, Deployment, Service, ConfigMap, and Ingress manifests exist.
- [x] Deployment has 2 replicas.
- [x] CPU and memory requests/limits are configured.
- [x] Liveness and readiness probes use `/health`.
- [x] Ingress host is `task-manager.local`.
- [x] `k8s/README.md` explains deployment and validation.

## Task 5: CI/CD

- [x] `.github/workflows/ci.yml` triggers on push and pull request to `main`.
- [x] Pipeline includes lint, test, Docker build, and Trivy security scan.
- [x] Image tag format is `ghcr.io/<username>/task-manager-api:<sha>`.
- [x] CI badge is documented in `README.md`.

## Final submission commit

- [x] Final repository state is ready for review.

# 任务管理器 API

[![CI](https://github.com/<your-username>/task-manager-api/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/task-manager-api/actions/workflows/ci.yml)

一个使用 Python 3.11 和 FastAPI 构建的 RESTful 任务管理器 API。该服务支持任务的增删改查、健康检查、内存存储、请求参数验证、结构化 JSON 错误响应、请求日志、Swagger/OpenAPI 文档、单元测试、Docker 容器化、Minikube Kubernetes 部署，以及 GitHub Actions CI/CD。

> 创建 GitHub 仓库后，请将 CI 徽章中的 `<your-username>` 替换为你的 GitHub 用户名。

## 技术栈

| 领域 | 技术 |
| --- | --- |
| API 框架 | Python 3.11+、FastAPI、Pydantic |
| 服务器 | Uvicorn |
| 测试 | pytest、pytest-cov |
| 代码检查 | pylint |
| 容器 | Docker、Docker Compose |
| Kubernetes | Minikube、kubectl、Ingress |
| CI/CD | GitHub Actions、Trivy、GHCR |

## 项目结构

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

## API 端点

| 方法 | 路径 | 说明 | 状态码 |
| --- | --- | --- | --- |
| GET | `/health` | 健康检查 | 200 |
| GET | `/tasks` | 获取全部任务 | 200 |
| GET | `/tasks/{id}` | 获取单个任务 | 200 / 404 |
| POST | `/tasks` | 创建任务 | 201 / 400 |
| PUT | `/tasks/{id}` | 更新任务 | 200 / 404 |
| DELETE | `/tasks/{id}` | 删除任务 | 204 / 404 |

Swagger UI 地址：

```bash
http://localhost:8080/docs
```

OpenAPI JSON 地址：

```bash
http://localhost:8080/openapi.json
```

## 任务数据模型

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

## 本地开发

### 1. 创建虚拟环境

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 2. 启动 API

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8080
```

### 3. 验证健康检查

```bash
curl http://localhost:8080/health
```

预期响应示例：

```json
{
  "status": "ok",
  "service": "task-manager-api",
  "timestamp": "2026-01-01T00:00:00+00:00"
}
```

## API 使用示例

### 创建任务

```bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Write Kubernetes manifests","description":"Create namespace, deployment, service, configmap, ingress","status":"todo"}'
```

预期状态：`201 Created`。

### 获取任务列表

```bash
curl http://localhost:8080/tasks
```

### 获取单个任务

```bash
curl http://localhost:8080/tasks/<task-id>
```

### 更新任务

```bash
curl -X PUT http://localhost:8080/tasks/<task-id> \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

### 删除任务

```bash
curl -X DELETE http://localhost:8080/tasks/<task-id>
```

预期状态：`204 No Content`。

## 运行测试和覆盖率检查

```bash
pytest
```

当前配置的最低测试覆盖率为 60%：

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=60
```

## 代码检查

```bash
pylint src --fail-under=8.0
```

## 运行时配置

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `SERVICE_NAME` | `task-manager-api` | `/health` 接口返回的服务名称 |
| `PORT` | `8080` | Docker 启动命令使用的 HTTP 监听端口 |
| `HOST` | `0.0.0.0` | Docker 启动命令使用的 HTTP 绑定地址 |
| `LOG_LEVEL` | `INFO` | Python 日志级别 |
| `RATE_LIMIT_PER_MINUTE` | `100` | 基于客户端和请求路径的滑动窗口每分钟限流数量 |

## Docker

### 构建镜像

```bash
docker build -t task-manager-api .
```

### 运行容器

```bash
docker run --rm -p 8080:8080 task-manager-api
```

### 验证服务

```bash
curl http://localhost:8080/health
```

### Docker Compose

```bash
docker compose up --build
```

## 使用 Minikube 部署 Kubernetes

详细说明请参阅 [`k8s/README.md`](k8s/README.md)。

快速开始：

```bash
minikube start
minikube addons enable ingress
docker build -t task-manager-api:latest .
minikube image load task-manager-api:latest
kubectl apply -f k8s/
kubectl rollout status deployment/task-manager-api -n task-manager
kubectl get all -n task-manager
```

使用端口转发进行验证：

```bash
kubectl port-forward svc/task-manager-api -n task-manager 8080:8080
curl http://localhost:8080/health
curl http://localhost:8080/tasks
```

使用 Ingress 进行验证：

```bash
echo "$(minikube ip) task-manager.local" | sudo tee -a /etc/hosts
curl http://task-manager.local/health
curl http://task-manager.local/tasks
```

## CI/CD

GitHub Actions 工作流定义在 `.github/workflows/ci.yml` 中，并在以下情况下运行：

- 向 `main` 分支推送代码
- 创建或更新目标分支为 `main` 的 Pull Request

流水线阶段：

1. 使用 `pylint` 进行代码检查
2. 使用 `pytest` 运行测试并检查覆盖率阈值
3. 构建 Docker 镜像
4. 使用 Trivy 扫描镜像
5. 在代码推送到 `main` 分支时，将镜像推送到 GHCR

Docker 镜像标签格式：

```text
ghcr.io/<username>/task-manager-api:<sha>
```

## Git 提交步骤

如果你使用了包含 Git 历史记录的压缩包，请创建一个名为 `task-manager-api` 的空白公开 GitHub 仓库，然后运行：

```bash
cd task-manager-api
git remote add origin https://github.com/<your-username>/task-manager-api.git
git push -u origin main
git push origin feature/api feature/container-k8s feature/ci-docs v1.0.0
```

如果你没有使用所提供的 Git 历史记录，请在提交前自行创建功能分支，并使用 Conventional Commits 规范提交代码。

推荐的最终提交信息：

```text
feat: complete homework submission
```

## 注意事项

- 按照作业要求，数据存储在内存中，因此进程重启后任务数据会被清空。
- 仓库中不包含密钥、令牌、密码或私钥。
- 如需提交截图，可以截取 `kubectl get all -n task-manager` 的输出以及成功的 API 响应，并按需添加到 README 中。

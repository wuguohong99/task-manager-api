作业提交检查清单
========

在提交 GitHub 仓库链接之前，请使用此清单进行检查。
任务 1：Git 与仓库
------------

- [ ] 仓库为公开仓库，名称为 `task-manager-api`。

- [ ] 存在 `README.md`，并包含本地运行、Docker、Kubernetes 和 CI 使用说明。

- [ ] 存在以下分支：`main`，以及至少两个 `feature/*` 分支。

- [ ] 提交信息遵循 Conventional Commits 规范。

- [ ] 最终提交信息为 `feat: complete homework submission`。

- [ ] `.gitignore` 已排除虚拟环境、IDE 文件、日志和构建产物。

任务 2：REST API
-------------

* [ ] `GET /health` 返回 HTTP 200。

* [ ] `GET /tasks` 返回全部任务。

* [ ] `GET /tasks/{id}` 返回 HTTP 200 或 404。

* [ ] `POST /tasks` 返回 HTTP 201 或 400。

* [ ] `PUT /tasks/{id}` 返回 HTTP 200 或 404。

* [ ] `DELETE /tasks/{id}` 返回 HTTP 204 或 404。

* [ ] JSON 数据模型包含 `id`、`title`、`description`、`status`、`created_at`、`updated_at`。

* [ ] 已包含请求验证、错误处理、请求日志、Swagger 文档、测试和限流功能。

任务 3：Docker
-----------

* [ ] `Dockerfile` 使用多阶段构建。

* [ ] 运行时镜像使用官方 `python:3.11-slim` 基础镜像。

* [ ] 应用以非 root 用户身份运行。

* [ ] 端口可通过 `PORT` 配置，默认值为 8080。

* [ ] 已包含 `.dockerignore`。

* [ ] 已包含 `docker-compose.yml`。

任务 4：Kubernetes
---------------

* [ ] 已包含 Namespace、Deployment、Service、ConfigMap 和 Ingress 清单文件。

* [ ] Deployment 配置了 2 个副本。

* [ ] 已配置 CPU 和内存的 requests/limits。

* [ ] 存活探针和就绪探针均使用 `/health`。

* [ ] Ingress 主机名为 `task-manager.local`。

* [ ] `k8s/README.md` 中包含部署和验证说明。

任务 5：CI/CD
----------

* [ ] `.github/workflows/ci.yml` 会在推送到 `main` 分支以及针对 `main` 分支创建 Pull Request 时触发。

* [ ] 流水线包含代码检查、测试、Docker 构建和 Trivy 安全扫描。

* [ ] 镜像标签格式为 `ghcr.io/<username>/task-manager-api:<sha>`。

* [ ] `README.md` 中已包含 CI 徽章说明。

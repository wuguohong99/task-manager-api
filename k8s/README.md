# Kubernetes / Minikube 部署

此目录包含将任务管理器 API 部署到本地 Minikube 集群所需的全部清单文件。

## 1. 启动 Minikube 并启用 Ingress

```bash
minikube start
minikube addons enable ingress
```

## 2. 为 Minikube 构建或加载镜像

方案 A：直接在 Minikube 的 Docker 守护进程中构建镜像：

```bash
eval $(minikube docker-env)
docker build -t task-manager-api:latest .
```

方案 B：在本地构建镜像并加载到 Minikube：

```bash
docker build -t task-manager-api:latest .
minikube image load task-manager-api:latest
```

## 3. 应用清单文件

```bash
kubectl apply -f k8s/
```

## 4. 验证资源

```bash
kubectl get all -n task-manager
kubectl get pods -n task-manager
kubectl rollout status deployment/task-manager-api -n task-manager
```

预期结果：Deployment 有 2 个已就绪的副本，并且 Pod 状态为 `Running`。

## 5. 使用端口转发进行测试

```bash
kubectl port-forward svc/task-manager-api -n task-manager 8080:8080
curl http://localhost:8080/health
curl http://localhost:8080/tasks
```

## 6. 使用 Ingress 主机名进行测试

将 Minikube IP 添加到 hosts 文件：

```bash
echo "$(minikube ip) task-manager.local" | sudo tee -a /etc/hosts
```

然后调用 API：

```bash
curl http://task-manager.local/health
curl http://task-manager.local/tasks
```

如果你在 macOS 或 Linux 上使用 Docker 驱动，并且无法直接访问 Ingress，请运行：

```bash
minikube tunnel
```

## 清理资源

```bash
kubectl delete -f k8s/
minikube stop
```

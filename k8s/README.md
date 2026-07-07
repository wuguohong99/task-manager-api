# Kubernetes / Minikube Deployment

This directory contains all manifests required to deploy the Task Manager API into a local Minikube cluster.

## 1. Start Minikube and enable Ingress

```bash
minikube start
minikube addons enable ingress
```

## 2. Build or load the image for Minikube

Option A: build directly inside Minikube's Docker daemon:

```bash
eval $(minikube docker-env)
docker build -t task-manager-api:latest .
```

Option B: build locally and load the image:

```bash
docker build -t task-manager-api:latest .
minikube image load task-manager-api:latest
```

## 3. Apply manifests

```bash
kubectl apply -f k8s/
```

## 4. Verify resources

```bash
kubectl get all -n task-manager
kubectl get pods -n task-manager
kubectl rollout status deployment/task-manager-api -n task-manager
```

Expected result: the deployment has 2 ready replicas and the pods are Running.

## 5. Test with port-forward

```bash
kubectl port-forward svc/task-manager-api -n task-manager 8080:8080
curl http://localhost:8080/health
curl http://localhost:8080/tasks
```

## 6. Test with Ingress host

Add the Minikube IP to your hosts file:

```bash
echo "$(minikube ip) task-manager.local" | sudo tee -a /etc/hosts
```

Then call the API:

```bash
curl http://task-manager.local/health
curl http://task-manager.local/tasks
```

If you use the Docker driver on macOS or Linux and Ingress is not reachable directly, run:

```bash
minikube tunnel
```

## Cleanup

```bash
kubectl delete -f k8s/
minikube stop
```

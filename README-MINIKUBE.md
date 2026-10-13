# CloudPulse on Minikube (Phase 2)

This adds Kubernetes manifests for the CloudPulse starter.

## Prerequisites
- Docker Desktop running
- Minikube cluster running
- kubectl configured for the Minikube context

Check first:

```powershell
minikube status
kubectl get nodes
```

If your cluster is stopped, start it with your existing profile:

```powershell
minikube start --driver=docker --cpus=2 --memory=3072
```

On an 8 GB PC, start with only the app, PostgreSQL and Redis. Do not install Argo CD and the full monitoring stack yet.

## Build the image inside Minikube

Run these commands from the project root (the folder containing `Dockerfile`):

```powershell
minikube image build -t cloudpulse:0.1.0 .
```

This builds the same image for the API and worker and makes it available to Minikube without pushing it to a registry.

## Deploy

Copy the `k8s` folder from this package into the CloudPulse project root, then run from the project root:

```powershell
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/10-config.yaml
kubectl apply -f k8s/20-postgres.yaml
kubectl apply -f k8s/30-redis.yaml
kubectl rollout status deployment/cloudpulse-postgres -n cloudpulse --timeout=180s
kubectl rollout status deployment/cloudpulse-redis -n cloudpulse --timeout=120s
kubectl apply -f k8s/40-api.yaml
kubectl apply -f k8s/50-worker.yaml
kubectl rollout status deployment/cloudpulse-api -n cloudpulse --timeout=180s
kubectl rollout status deployment/cloudpulse-worker -n cloudpulse --timeout=120s
kubectl get pods,svc,pvc -n cloudpulse
```

## Open the app

In a terminal, keep this running:

```powershell
kubectl port-forward -n cloudpulse svc/cloudpulse-api 8000:8000
```

Then open http://localhost:8000. API docs: http://localhost:8000/docs. Metrics: http://localhost:8000/metrics.

## Test a job

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/jobs -ContentType "application/json" -Body '{"task":"Run Minikube smoke test"}'
Start-Sleep -Seconds 4
Invoke-RestMethod http://localhost:8000/jobs
```

## Troubleshooting

```powershell
kubectl get pods -n cloudpulse
kubectl describe pod -n cloudpulse <POD_NAME>
kubectl logs -n cloudpulse deployment/cloudpulse-api
kubectl logs -n cloudpulse deployment/cloudpulse-worker
kubectl logs -n cloudpulse deployment/cloudpulse-postgres
kubectl logs -n cloudpulse deployment/cloudpulse-redis
kubectl get events -n cloudpulse --sort-by=.metadata.creationTimestamp
```

If the API pod restarts, check its logs and confirm PostgreSQL and Redis are Ready first. For image errors, rebuild with `minikube image build -t cloudpulse:0.1.0 .` and check `imagePullPolicy: IfNotPresent`.

## Clean up

Delete only this project's Kubernetes resources:

```powershell
kubectl delete namespace cloudpulse
```

This removes the namespace and its PVC/data. Do not run it if you need the local database contents.

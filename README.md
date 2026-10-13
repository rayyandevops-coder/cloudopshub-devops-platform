# CloudOpsHub — Cloud-Native DevOps Platform

CloudOpsHub is a hands-on DevOps/SRE portfolio project built around a Python FastAPI service. It demonstrates containerization, automated checks and image publishing, Kubernetes deployment with Helm, and GitOps reconciliation with Argo CD.

> **Current verified demo state (Minikube):** the API runs in the `cloudopshub` namespace; its Deployment has one ready replica; the Argo CD Application reports `Synced` and `Healthy`; and `/health` returns `{"status":"healthy","service":"cloudopshub"}`.

## What is implemented and verified

- FastAPI service with health, readiness, info, items, and Prometheus metrics endpoints.
- Docker image published to GitHub Container Registry (GHCR).
- GitHub Actions checks for Python tests, Hadolint, Trivy filesystem scanning, image build, Trivy image scanning, and image publishing.
- Helm chart under `helm/cloudopshub` for the Deployment and ClusterIP Service.
- Argo CD Application in `argocd/application.yaml` watching `main` and the `helm/cloudopshub` path, with automated sync, pruning, and self-healing enabled.
- Kubernetes health/readiness probes and resource requests/limits.
- Prometheus-compatible metrics exposed by the application.

The repository also contains learning/configuration material for additional tools. Only claim an AWS/Terraform, Ansible, GitLab, load-testing, or Grafana capability as completed in an interview when you have run and captured evidence for that specific component.

## Architecture

```mermaid
flowchart TD
    Dev[Developer pushes to GitHub] --> CI[GitHub Actions]
    CI --> Tests[Pytest + Hadolint + Trivy filesystem scan]
    Tests --> Build[Build container image]
    Build --> Scan[Trivy image scan]
    Scan --> GHCR[Push SHA-tagged and latest images to GHCR]
    Git[Git repository: Helm chart] --> Argo[Argo CD]
    Argo --> K8s[Kubernetes / Minikube]
    GHCR -. image pulled by .-> Pod[CloudOpsHub FastAPI Pod]
    K8s --> Svc[ClusterIP Service :80 → container :8000]
    Svc --> API[FastAPI endpoints]
    API --> Health[/health and /ready]
    API --> Metrics[/metrics]
```

**Important CI/CD distinction:** GitHub Actions builds, scans, and publishes the image. Argo CD continuously reconciles Kubernetes resources from the committed Helm chart. The current chart refers to the `latest` image tag, so publishing a new image alone does not necessarily trigger a new Pod rollout. For a stronger production pattern, use the immutable commit-SHA image tag and commit/update that tag in the Helm values (or use a dedicated image updater).

## Repository layout

```text
.
├── app/                         # FastAPI application
├── tests/                       # API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .github/workflows/ci-cd.yml  # CI, security scans, image publishing
├── .gitlab-ci.yml               # Alternative CI example
├── k8s/                         # Raw Kubernetes manifests/examples
├── helm/cloudopshub/            # Helm chart used by Argo CD
├── argocd/application.yaml      # Argo CD Application
├── monitoring/                  # Monitoring configuration
├── monitoring-values.yaml       # Prometheus Helm values used in the demo
├── terraform/                   # Terraform configuration/examples
├── ansible/                     # Ansible configuration/examples
├── loadtest/                    # k6 test scripts
├── scripts/                     # Operational scripts
└── docs/                        # Project notes
```

## API endpoints

With the application reachable at `http://localhost:8001`:

| Endpoint | Purpose |
|---|---|
| `/` | Root/status response |
| `/health` | Liveness health check |
| `/ready` | Readiness check |
| `/api/v1/info` | Service information |
| `/api/v1/items` | Example items endpoint |
| `/metrics` | Prometheus-format application metrics |
| `/docs` | FastAPI Swagger UI |

The exact endpoint responses are defined in `app/main.py` and tested in `tests/test_api.py`.

## Run tests locally (Windows PowerShell)

A virtual environment avoids conflicts with globally installed Python packages.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

Expected test result for the current test suite: `5 passed`.

## Build and run the container

```powershell
docker build -t cloudopshub:local .
docker run --rm -p 8000:8000 cloudopshub:local
```

Then test `http://localhost:8000/health`. For local Compose options, review `docker-compose.yml` and `.env.example` before starting the stack.

## CI/CD workflow

The workflow `.github/workflows/ci-cd.yml` runs on pushes and pull requests targeting `main`:

1. Install Python dependencies and run `python -m pytest -q`.
2. Lint `Dockerfile` with Hadolint.
3. Scan the repository filesystem using Trivy.
4. On a push to `main`, build the image with both the commit SHA and `latest` tags.
5. Scan the built image with Trivy; the scan fails on HIGH or CRITICAL findings.
6. Push both tags to `ghcr.io/rayyandevops-coder/cloudopshub-devops-platform`.

The successful run used for the current demo can be viewed here: [GitHub Actions run](https://github.com/rayyandevops-coder/cloudopshub-devops-platform/actions/runs/38418160118).

## Kubernetes / Helm deployment

The active Argo CD Application deploys the Helm chart into the `cloudopshub` namespace. The current chart configuration has one replica and disables Ingress, so local access is provided with `kubectl port-forward`.

Check status:

```powershell
kubectl get application cloudopshub -n argocd
kubectl get deployment,pods,svc -n cloudopshub
```

Lint/render the chart:

```powershell
helm lint .\helm\cloudopshub
helm template cloudopshub .\helm\cloudopshub --namespace cloudopshub
```

## Access the API through port-forward

Run this in a terminal and keep it open:

```powershell
kubectl port-forward -n cloudopshub svc/cloudopshub-cloudopshub 8001:80
```

In another terminal:

```powershell
curl.exe -i http://localhost:8001/health
curl.exe -i http://localhost:8001/ready
curl.exe -i http://localhost:8001/api/v1/info
curl.exe -i http://localhost:8001/api/v1/items
```

Expected health response:

```json
{"status":"healthy","service":"cloudopshub"}
```

## Argo CD / GitOps

The Application definition lives at `argocd/application.yaml` and references:

- Git repository: `https://github.com/rayyandevops-coder/cloudopshub-devops-platform.git`
- Branch: `main`
- Chart path: `helm/cloudopshub`
- Destination namespace: `cloudopshub`
- Sync policy: automated sync, prune, and self-heal

Check the state:

```powershell
kubectl get application cloudopshub -n argocd
```

Open the local dashboard by running:

```powershell
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Then browse to `https://localhost:8081`. Keep credentials out of source control. Rotate the initial admin password if it was exposed in terminal captures or chat.

### Demonstrate reconciliation and self-healing

1. Change a setting such as `replicaCount` in `helm/cloudopshub/values.yaml`.
2. Commit and push the change to `main`.
3. Wait for Argo CD to reconcile.
4. Verify `Synced` / `Healthy` and check the Deployment replica count.
5. Optionally make a temporary manual replica change and verify that Argo CD self-healing restores the Git-declared replica count.

Do this only in your local development cluster.

## Monitoring

The application exposes Prometheus metrics at `/metrics`. The repository includes `monitoring-values.yaml`; the demo previously installed Prometheus and Grafana in the `monitoring` namespace. To avoid excess laptop load, start these components only when actively demonstrating monitoring. Do not delete system namespaces to reduce resource use.

## Resource and troubleshooting commands

```powershell
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe application cloudopshub -n argocd
kubectl logs deployment/cloudopshub-cloudopshub -n cloudopshub --tail=80
helm list -A
```

For Minikube, `kubectl top` requires Metrics Server to be running. If it returns `Metrics API not available`, check the Metrics Server add-on before treating it as an application error.

## Current demo evidence

- GitHub Actions: latest recorded workflow run succeeded, including test, Hadolint, Trivy filesystem scan, image build, Trivy image scan, and GHCR push.
- Kubernetes: `cloudopshub-cloudopshub` Deployment has one ready replica.
- API: `/health` returned `{"status":"healthy","service":"cloudopshub"}` and `/ready` returned a ready response.
- Argo CD: Application `cloudopshub` reported `Synced` and `Healthy`.

## Resume-ready project summary

**CloudOpsHub — Cloud-Native DevOps Platform**

- Built and containerized a FastAPI service with health/readiness endpoints and Prometheus-compatible metrics.
- Implemented GitHub Actions CI/CD with pytest, Hadolint, Trivy filesystem and image scans, and publishing to GitHub Container Registry.
- Deployed the service to Minikube using Kubernetes and Helm, with Argo CD automated sync and self-healing from Git.
- Validated API health and readiness and demonstrated Git-driven replica changes through the GitOps workflow.

Only include additional AWS/Terraform, Ansible, Grafana, or load-testing accomplishments on a resume after validating and capturing evidence for those parts.

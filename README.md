# CloudOpsHub — Production-Style Cloud Native DevOps Platform

CloudOpsHub is a portfolio-grade DevOps/SRE project designed to demonstrate an end-to-end software delivery and operations workflow using the tools in my DevOps profile.

## What this project demonstrates

- Python FastAPI REST API
- Docker containerization
- Multi-stage image build
- GitHub Actions CI/CD
- GitLab CI/CD alternative pipeline
- Trivy container/image security scanning
- Hadolint Dockerfile linting
- k6 load testing
- Kubernetes Deployments, Services, ConfigMaps, Secrets, Ingress and PersistentVolume
- Helm packaging
- Argo CD GitOps deployment
- Terraform AWS infrastructure
- Ansible server bootstrap
- Prometheus metrics
- Grafana dashboard provisioning
- Linux/Bash operational scripts
- Health checks, structured logging and rollback-oriented deployment flow

## Architecture

```text
Developer
   |
   v
GitHub
   |
   +--> GitHub Actions
   |      |- lint
   |      |- test
   |      |- Hadolint
   |      |- Trivy
   |      |- Docker build/push
   |      `- deploy/update GitOps image tag
   |
   v
Container Registry
   |
   v
Kubernetes
   |
   +--> Ingress --> CloudOpsHub API
   |
   +--> Service --> FastAPI Pods
   |                  |
   |                  +--> /health
   |                  +--> /ready
   |                  `--> /metrics
   |
   +--> Prometheus
   |
   `--> Grafana

AWS path:
Terraform --> VPC --> EC2 --> Kubernetes/bootstrap resources
Ansible  --> Linux server configuration
Argo CD  --> Helm/Kubernetes GitOps deployment
```

## Repository layout

```text
cloudopshub/
├── app/                    # FastAPI application
├── tests/                  # Unit/API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── .hadolint.yaml
├── .env.example
├── .github/workflows/      # GitHub Actions
├── .gitlab-ci.yml          # GitLab CI alternative
├── k8s/                    # Raw Kubernetes manifests
├── helm/cloudopshub/       # Helm chart
├── argocd/                 # Argo CD Application + GitOps values
├── monitoring/             # Prometheus/Grafana configuration
├── terraform/aws/          # AWS IaC
├── ansible/                # Linux configuration
├── scripts/                # Operations scripts
└── loadtest/               # k6 performance test
```

## Run locally

### 1. Clone

```bash
git clone https://github.com/<YOUR_USERNAME>/cloudopshub-devops-platform.git
cd cloudopshub-devops-platform
```

### 2. Run with Docker Compose

```bash
cp .env.example .env
docker compose up --build -d
```

API:
- http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

Prometheus:
- http://localhost:9090

Grafana:
- http://localhost:3000
- default local credentials: admin / admin

### 3. Test

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/info
curl http://localhost:8000/api/v1/items
```

Run tests:

```bash
python -m pip install -r requirements.txt
pytest -q
```

## Docker security

Lint:

```bash
docker run --rm -i hadolint/hadolint < Dockerfile
```

Build:

```bash
docker build -t cloudopshub:local .
```

Scan:

```bash
trivy image cloudopshub:local
```

## Kubernetes deployment

The raw manifests are under `k8s/`.

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

kubectl -n cloudopshub get pods,svc,ingress
```

> `k8s/secret.yaml` contains only a demo placeholder. Never commit production credentials.

## Helm

```bash
helm lint helm/cloudopshub
helm template cloudopshub helm/cloudopshub
helm upgrade --install cloudopshub helm/cloudopshub \
  --namespace cloudopshub --create-namespace
```

## Argo CD / GitOps

Edit `argocd/application.yaml` and replace:

```text
YOUR_GITHUB_USERNAME/cloudopshub-devops-platform
```

with your actual GitHub repository.

Then:

```bash
kubectl apply -f argocd/application.yaml
```

Argo CD will reconcile the Helm release from Git.

## AWS Terraform

The Terraform stack is intentionally conservative and uses variables so that credentials and environment-specific values stay outside source control.

```bash
cd terraform/aws
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

For a real AWS deployment, review the VPC CIDRs, instance size, SSH access rules and estimated cost before applying.

Destroy when finished:

```bash
terraform destroy
```

## Ansible

Configure `ansible/inventory.ini` with the target host:

```ini
[k8s]
YOUR_SERVER ansible_user=ubuntu
```

Test connectivity:

```bash
ansible -i ansible/inventory.ini k8s -m ping
```

Run:

```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

## k6 load test

Install k6, start the API, then:

```bash
k6 run loadtest/smoke.js
```

The test exercises health, API information and item endpoints.

## CI/CD

### GitHub Actions

`.github/workflows/ci-cd.yml` performs:

1. Python dependency installation
2. Unit tests
3. Dockerfile linting with Hadolint
4. Docker image build
5. Trivy filesystem/image security checks
6. Image publication to GHCR
7. GitOps image-tag update when deployment secrets are configured

Required repository secrets for registry/GitOps deployment are documented in `.github/workflows/ci-cd.yml`.

### GitLab CI

`.gitlab-ci.yml` provides the same conceptual stages:

```text
test -> security -> build -> deploy
```

It can be enabled when the repository is mirrored to GitLab.

## Monitoring

FastAPI exposes Prometheus-compatible metrics at:

```text
/metrics
```

The monitoring stack demonstrates:

- request count
- request latency
- process metrics
- API availability
- Prometheus scraping
- Grafana visualization

## Operational scripts

```bash
./scripts/health-check.sh
./scripts/backup-config.sh
./scripts/rollback-k8s.sh
```

The scripts are intentionally simple enough to explain during an interview.

## Suggested demo flow for interviews

1. Show the GitHub repository structure.
2. Explain the architecture diagram.
3. Run the API locally with Docker Compose.
4. Open `/docs`, `/health` and `/metrics`.
5. Push a small code change.
6. Show GitHub Actions test/security/build stages.
7. Show the image in GHCR.
8. Deploy with Helm/Argo CD.
9. Show Kubernetes pods and rollout history.
10. Open Prometheus/Grafana.
11. Run k6 and discuss latency/availability.
12. Explain how Terraform and Ansible make the environment reproducible.

## Resume-ready project entry

**CloudOpsHub — Cloud-Native DevOps & SRE Platform**
- Built and containerized a Python FastAPI service with Docker and automated CI/CD using GitHub Actions and GitLab CI/CD.
- Deployed the application to Kubernetes using Deployments, Services, ConfigMaps, Secrets, Ingress and PersistentVolumes, packaged with Helm and reconciled through Argo CD GitOps.
- Provisioned AWS infrastructure with Terraform and automated Linux server configuration using Ansible.
- Implemented Prometheus/Grafana observability, Trivy security scanning, Hadolint Dockerfile linting and k6 performance testing.

## Important portfolio note

This repository is a realistic portfolio project, but do not claim AWS/Argo CD/Kubernetes production usage unless you actually deploy and demonstrate those components. The strongest presentation is to deploy the stack yourself and capture screenshots/logs as evidence.

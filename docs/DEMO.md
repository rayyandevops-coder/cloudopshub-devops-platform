# 10-Minute Demo Checklist

1. `docker compose up --build -d`
2. Open `http://localhost:8000/docs`
3. Run `curl http://localhost:8000/health`
4. Run `docker compose ps`
5. Open Prometheus at `http://localhost:9090`
6. Open Grafana at `http://localhost:3000`
7. Run `k6 run loadtest/smoke.js`
8. Show `.github/workflows/ci-cd.yml`
9. Show `helm/cloudopshub`
10. Show `argocd/application.yaml`
11. Show Terraform plan/outputs
12. Explain rollback and observability

## Screenshot evidence worth capturing

- GitHub Actions green pipeline
- GHCR image/tag
- `kubectl get pods -n cloudopshub`
- `kubectl rollout history deployment/cloudopshub -n cloudopshub`
- Helm release
- Argo CD synced/healthy application
- Prometheus targets
- Grafana dashboard
- k6 result
- Terraform plan

# Interview Walkthrough

## 1. Why this project?

The project combines application delivery, infrastructure automation, container orchestration, security and observability in one reproducible repository.

## 2. CI/CD explanation

A commit to `main` triggers GitHub Actions. Tests run first. Dockerfile linting and Trivy scanning protect the build. A successful build is pushed to GHCR. In a full GitOps setup, Argo CD watches the repository and reconciles the Helm deployment.

## 3. Why Kubernetes?

Kubernetes gives the application declarative deployments, self-healing, rolling updates, service discovery and readiness/liveness probes.

## 4. Why Helm?

Helm makes Kubernetes configuration reusable and environment-aware instead of maintaining many duplicated YAML files.

## 5. Why Argo CD?

Argo CD makes Git the desired state for deployment. Changes can be reviewed in Git and automatically reconciled by the cluster.

## 6. Why Terraform + Ansible?

Terraform manages cloud resources declaratively. Ansible handles operating-system configuration after infrastructure exists. This separates infrastructure provisioning from server configuration.

## 7. Monitoring

Prometheus scrapes `/metrics`. Grafana visualizes the time series. The API also has `/health` and `/ready` endpoints so Kubernetes and operators can distinguish process health from readiness.

## 8. Security

Trivy scans the source filesystem and built container image. Hadolint checks Dockerfile practices. Kubernetes Secrets are separated from normal ConfigMaps, and the Terraform SSH CIDR is parameterized.

## 9. Performance

k6 sends concurrent traffic and validates error rate and p95 latency thresholds. This provides a repeatable performance baseline rather than a subjective test.

## 10. Failure/rollback story

If a deployment is unhealthy, Kubernetes readiness probes prevent bad pods from receiving traffic. `kubectl rollout status` verifies the rollout, and the provided rollback script can revert to the previous revision.

## 11. What I would improve for production

- Use AWS EKS rather than a self-managed Kubernetes node.
- Store secrets in AWS Secrets Manager/External Secrets.
- Use a private container registry or strict GHCR access controls.
- Add TLS with cert-manager.
- Add centralized logs with OpenSearch/Loki.
- Add SLOs, alert rules and on-call routing.
- Add Terraform remote state with locking.
- Add separate staging and production environments.
- Add dependency/SBOM scanning and image signing.

#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-cloudopshub}"
DEPLOYMENT="${DEPLOYMENT:-cloudopshub}"

kubectl -n "${NAMESPACE}" rollout history deployment/"${DEPLOYMENT}"
kubectl -n "${NAMESPACE}" rollout undo deployment/"${DEPLOYMENT}"
kubectl -n "${NAMESPACE}" rollout status deployment/"${DEPLOYMENT}"

echo "Rollback completed."

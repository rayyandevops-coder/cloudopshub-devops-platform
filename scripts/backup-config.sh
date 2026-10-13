#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "${BACKUP_DIR}"
tar -czf "${BACKUP_DIR}/cloudopshub-config-${TIMESTAMP}.tar.gz" \
  k8s helm argocd monitoring terraform ansible

echo "Backup created: ${BACKUP_DIR}/cloudopshub-config-${TIMESTAMP}.tar.gz"

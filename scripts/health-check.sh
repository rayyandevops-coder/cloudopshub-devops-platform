#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "Checking CloudOpsHub at ${BASE_URL}"

for endpoint in /health /ready /api/v1/info /metrics; do
  echo "GET ${endpoint}"
  curl --fail --silent --show-error "${BASE_URL}${endpoint}" >/dev/null
  echo "OK"
done

echo "All health checks passed."

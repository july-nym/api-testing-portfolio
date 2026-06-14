#!/usr/bin/env bash
# Newman CLI runner.
#
# Usage:
#   ./run-newman.sh                # dev environment
#   ./run-newman.sh staging        # staging environment
#
# Picks the environment by name, emits a CLI summary plus a JUnit XML report so
# CI can surface per-request results. --delay-request keeps the free Heroku dyno
# behind restful-booker from rate-limiting us on a fast burst.
set -euo pipefail

ENV_NAME="${1:-dev}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

COLLECTION="${SCRIPT_DIR}/api-portfolio.postman_collection.json"
ENV_FILE="${SCRIPT_DIR}/environments/${ENV_NAME}.postman_environment.json"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "No environment file for '${ENV_NAME}' (looked for ${ENV_FILE})" >&2
  exit 1
fi

mkdir -p "${SCRIPT_DIR}/reports"

newman run "${COLLECTION}" \
  --environment "${ENV_FILE}" \
  --delay-request 250 \
  --reporters cli,junit \
  --reporter-junit-export "${SCRIPT_DIR}/reports/newman-${ENV_NAME}.xml"

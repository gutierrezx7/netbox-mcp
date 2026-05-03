#!/usr/bin/env bash
set -euo pipefail

# E2E create script (non-destructive by default)
# Requires: NETBOX_URL, NETBOX_TOKEN
# To actually execute, set RUN_E2E=true in the environment.

if [ -z "${NETBOX_URL:-}" ] || [ -z "${NETBOX_TOKEN:-}" ]; then
  echo "ERROR: NETBOX_URL and NETBOX_TOKEN must be set"
  exit 2
fi

RUN=${RUN_E2E:-false}

payload='{"name": "e2e-test-site", "slug": "e2e-test-site"}'
cmd=(curl -sS -X POST -H "Authorization: Token ${NETBOX_TOKEN}" -H "Content-Type: application/json" -d "$payload" "${NETBOX_URL%/}/api/dcim/sites/")

echo "E2E create (dry-run). Command: ${cmd[*]}"
if [ "$RUN" = "true" ]; then
  echo "Executing create..."
  ${cmd[@]} | jq .
else
  echo "To execute: export RUN_E2E=true && ./scripts/e2e_create.sh"
fi

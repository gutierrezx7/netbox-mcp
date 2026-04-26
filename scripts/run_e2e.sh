#!/usr/bin/env bash
set -euo pipefail

# Simple E2E harness scaffold. Requires NETBOX_URL and NETBOX_TOKEN env vars.
if [ -z "${NETBOX_URL:-}" ] || [ -z "${NETBOX_TOKEN:-}" ]; then
  echo "ERROR: NETBOX_URL and NETBOX_TOKEN must be set in the environment to run E2E."
  echo "Example:"
  echo "  export NETBOX_URL=https://netbox.example.local"
  echo "  export NETBOX_TOKEN=changeme"
  exit 2
fi

echo "Running E2E scaffold against $NETBOX_URL"

echo "1) List sites (GET)"
curl -sS -H "Authorization: Token $NETBOX_TOKEN" "$NETBOX_URL/api/dcim/sites/?limit=1" | jq . || true

echo "2) Note: Create/Update/Delete steps require a real test tenant and are potentially destructive."
echo "   Use the e2e/README.md for guidance to implement non-destructive test scripts tailored to your environment."

echo "E2E scaffold complete. Review outputs above for connectivity and API access."

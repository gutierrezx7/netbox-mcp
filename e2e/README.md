# E2E Test Harness (NetBox LXC)

This directory contains scaffolding for end-to-end tests to run against a real
NetBox instance (e.g., LXC 1038). These are NOT executed in CI by default and
require network access and credentials.

Usage (manual):

1. Export environment variables pointing to the target NetBox instance:

   ```bash
   export NETBOX_URL=https://netbox.example.local
   export NETBOX_TOKEN=xxx
   ```

2. Run the harness script (adjust for your environment):

   ```bash
   ./run_e2e.sh --host https://netbox.example.local --token $NETBOX_TOKEN
   ```

The script will perform create/update/delete/search/changelog checks and report
results to stdout. It is intentionally simple and meant to be adapted to your
environment.

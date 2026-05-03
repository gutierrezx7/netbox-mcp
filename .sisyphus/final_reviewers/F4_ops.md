# F4 — Ops Reviewer

Goal: Validate deployment steps to MetaMCP and installation on LXC 1043.

Checklist:

1. Dockerfile build locally:

   ```bash
   docker build -t netbox-mcp:local .
   ```

2. Packaging: ensure entrypoint `netbox-mcp` works in container
3. Installation steps for LXC (documented in deploy.md)

Deliverables:
- Confirmation that image builds and runs, and documented installation steps.

# Deployment Guide — MetaMCP / LXC

This document describes steps to package and deploy the NetBox MCP server to a MetaMCP environment (LXC).

1) Build the Docker image locally (optional):

   docker build -t netbox-mcp:local .

2) Package for installation on LXC (if Docker not used):

   - Create a Python virtualenv on the target LXC
   - Install runtime deps: `pip install pydantic pydantic-settings httpx`
   - Copy `src/` into `/opt/netbox-mcp/` and create a systemd service or wrapper script that runs `python -m netbox_mcp_server`

3) Run as mcp-netbox user (recommended):

   sudo -u mcp-netbox -i
   cd /opt/netbox-mcp
   .venv/bin/python -m netbox_mcp_server

4) MetaMCP integration

   - Ensure the wrapper script registers the MCP tools with MetaMCP according to local conventions.
   - Provide env vars via systemd service or container environment: NETBOX_URL, NETBOX_TOKEN, etc.

5) Rollback

   - Keep previous image or archive copy to revert quickly.

Security

- Do not commit tokens; use `.env` files on host and ensure `.env` is in .gitignore.

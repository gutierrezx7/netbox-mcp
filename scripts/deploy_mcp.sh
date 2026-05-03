#!/usr/bin/env bash
set -euo pipefail

# Deployment helper (non-destructive template) for installing NetBox MCP on an LXC
# This script is a *template* and performs no destructive actions unless RUN_DEPLOY=true

if [ "$EUID" -ne 0 ]; then
  echo "This script should be run as root or via sudo on the target host (LXC)." >&2
fi

RUN=${RUN_DEPLOY:-false}
INSTALL_PATH=${INSTALL_PATH:-/opt/netbox-mcp}
VENV_PATH="$INSTALL_PATH/.venv"

echo "Deploy template: target path=$INSTALL_PATH  venv=$VENV_PATH"

echo "Prerequisites (to run manually):"
echo " - Create target user (mcp-netbox) and ensure it has access to $INSTALL_PATH" 
echo " - Ensure NETBOX_URL and NETBOX_TOKEN are provided via systemd unit or environment file"

echo "Planned steps (dry-run):"
cat <<'STEPS'
1) Create system user: useradd -r -s /usr/sbin/nologin mcp-netbox
2) Create install directory and set ownership to mcp-netbox
3) Create Python venv at $INSTALL_PATH/.venv and install runtime deps
4) Copy application source to $INSTALL_PATH/src
5) Create systemd unit to run `python -m netbox_mcp_server` as mcp-netbox
6) Reload systemd and enable/start service
7) Verify service logs and API connectivity
STEPS

if [ "$RUN" != "true" ]; then
  echo "Dry-run only. To execute real deployment set RUN_DEPLOY=true in the environment and re-run." 
  exit 0
fi

echo "Executing deployment steps..."

id -u mcp-netbox >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin mcp-netbox
mkdir -p "$INSTALL_PATH"
chown mcp-netbox:mcp-netbox "$INSTALL_PATH"

python3 -m venv "$VENV_PATH"
"$VENV_PATH/bin/pip" install --upgrade pip
"$VENV_PATH/bin/pip" install pydantic pydantic-settings httpx

cp -r src "$INSTALL_PATH/"
chown -R mcp-netbox:mcp-netbox "$INSTALL_PATH"

cat > /etc/systemd/system/netbox-mcp.service <<'UNIT'
[Unit]
Description=NetBox MCP Server
After=network.target

[Service]
Type=simple
User=mcp-netbox
WorkingDirectory=/opt/netbox-mcp
Environment=NETBOX_URL=
Environment=NETBOX_TOKEN=
ExecStart=/opt/netbox-mcp/.venv/bin/python -m netbox_mcp_server
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now netbox-mcp.service

echo "Deployment executed. Check service status: systemctl status netbox-mcp" 

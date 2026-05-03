# F1 — Functionality Reviewer

Goal: Verify that all 7 MCP tools are registered and functionally exercise core happy paths.

What to run (local machine with repo checked out and Python available):

1. Install dev deps:

   python -m pip install -r requirements.txt

2. Run unit tests:

   pytest tests/test_client.py::TestNetBoxRestClient -q

3. Smoke test core tools programmatically (example):

   python - <<'PY'
from netbox_mcp_server.config import get_settings
from netbox_mcp_server.client import NetBoxRestClient
from netbox_mcp_server.objects import netbox_get_objects
settings = get_settings()
client = NetBoxRestClient(settings.NETBOX_URL, settings.NETBOX_TOKEN, timeout=settings.TIMEOUT, rate_limit=0)
print('OK client created')
try:
    # non-destructive call example (will fail without NetBox)
    print('Attempting list (may error without NetBox):')
    print(netbox_get_objects(client, 'dcim.sites', filters={}, limit=1))
except Exception as e:
    print('Expected error (no NetBox):', e)
PY

Expected evidence to provide:
- pytest output for targeted functional tests (stdout capture)
- any interactive run outputs from the smoke test above
- note any failing tests and stack traces

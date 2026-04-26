# NetBox MCP Server - Full CRUD

This repository implements an MCP (Model Connector Plugin) server for NetBox
with full CRUD capabilities, search, and changelog retrieval. It provides a
small set of tools intended for automation, DevOps, and LLM-based integrations.

Quickstart
---------

1. Install dependencies (Python 3.11+ recommended):

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Configure environment variables (see `.env.example`).

3. Run tests:

   ```bash
   pytest -q
   ```

Usage example (programmatic)
-----------------------------

```python
from netbox_mcp_server.config import get_settings
from netbox_mcp_server.client import NetBoxRestClient
from netbox_mcp_server.objects import netbox_get_objects

settings = get_settings()
client = NetBoxRestClient(settings.NETBOX_URL, settings.NETBOX_TOKEN, timeout=settings.TIMEOUT, rate_limit=settings.RATE_LIMIT)
resp = netbox_get_objects(client, object_type='dcim.sites', filters={'name__icontains': 'prod'}, limit=10)
print(resp)
```

Project layout
--------------

See `src/netbox_mcp_server/` for implementation. Tests are under `tests/`.

Contributing
------------
Please open issues or pull requests. See CONTRIBUTING.md for guidelines.

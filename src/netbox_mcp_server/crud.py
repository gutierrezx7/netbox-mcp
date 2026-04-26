"""CRUD operations helpers for NetBox MCP.

Provides create/update/delete helpers that call the NetBox API via the
NetBoxRestClient.
"""
from typing import Any, Dict, List, Optional

from .types import NETBOX_OBJECT_TYPES
from .validators import parse_lookup_expressions
from .config import get_settings


def netbox_create_object(client, object_type: str, payload: Any) -> Dict[str, Any]:
    """Create single or bulk objects depending on payload type.

    If payload is a list, performs bulk creation by sending arrays in POST.
    Returns the JSON-decoded response from NetBox.
    """
    if object_type not in NETBOX_OBJECT_TYPES:
        raise ValueError(f"unknown object_type: {object_type}")

    endpoint = NETBOX_OBJECT_TYPES[object_type]
    path = f"/{endpoint}/"

    settings = get_settings()
    bulk_max = getattr(settings, "BULK_MAX", 100)

    # single create
    if not isinstance(payload, list):
        resp = client.post(path, json=payload)
        return resp.json()

    # bulk create (list)
    results = []
    # chunk the list into sizes of bulk_max
    for i in range(0, len(payload), bulk_max):
        chunk = payload[i:i+bulk_max]
        resp = client.post(path, json=chunk)
        try:
            data = resp.json()
        except Exception:
            data = None
        results.append(data)

    return {"bulk_results": results}

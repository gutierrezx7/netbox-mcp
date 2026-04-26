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


def netbox_update_object(client, object_type: str, payload: Any) -> Dict[str, Any]:
    """Update single or bulk objects. For single updates, payload is a dict with 'id' and fields.

    For bulk updates, payload is a list of dicts.
    """
    if object_type not in NETBOX_OBJECT_TYPES:
        raise ValueError(f"unknown object_type: {object_type}")

    endpoint = NETBOX_OBJECT_TYPES[object_type]
    settings = get_settings()
    bulk_max = getattr(settings, "BULK_MAX", 100)

    # single update
    if not isinstance(payload, list):
        obj_id = payload.get("id")
        if obj_id is None:
            raise ValueError("payload for single update must include 'id'")
        path = f"/{endpoint}{obj_id}/"
        resp = client.request("PATCH", path, json=payload)
        return resp.json()

    # bulk update - iterate
    results = []
    for i in range(0, len(payload), bulk_max):
        chunk = payload[i:i+bulk_max]
        # Depending on NetBox API, bulk patch may not be supported; this implementation
        # performs sequential patch calls per item to remain compatible.
        chunk_results = []
        for item in chunk:
            obj_id = item.get("id")
            if obj_id is None:
                chunk_results.append(None)
                continue
            path = f"/{endpoint}{obj_id}/"
            resp = client.request("PATCH", path, json=item)
            try:
                chunk_results.append(resp.json())
            except Exception:
                chunk_results.append(None)
        results.append(chunk_results)

    return {"bulk_results": results}


def netbox_delete_object(client, object_type: str, ids: Any) -> Dict[str, Any]:
    """Delete single or multiple objects.

    ids: single int id or list of ids
    """
    if object_type not in NETBOX_OBJECT_TYPES:
        raise ValueError(f"unknown object_type: {object_type}")

    endpoint = NETBOX_OBJECT_TYPES[object_type]

    if isinstance(ids, list):
        results = []
        for obj_id in ids:
            path = f"/{endpoint}{obj_id}/"
            resp = client.request("DELETE", path)
            results.append({"id": obj_id, "status_code": getattr(resp, 'status_code', None)})
        return {"deleted": results}

    # single
    path = f"/{endpoint}{ids}/"
    resp = client.request("DELETE", path)
    return {"id": ids, "status_code": getattr(resp, 'status_code', None)}

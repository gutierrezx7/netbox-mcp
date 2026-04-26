"""Search utilities for NetBox MCP.

Provides netbox_search_objects which performs a simple global search across
multiple NetBox object endpoints using the provided NetBoxRestClient.
"""
from typing import List, Optional, Dict, Any

from .types import NETBOX_OBJECT_TYPES


def netbox_search_objects(client, q: str, limit: int = 50, offset: int = 0, object_type: Optional[str] = None) -> Dict[str, Any]:
    """Search across NetBox object endpoints.

    Args:
        client: an instance of NetBoxRestClient (or compatible) with a `get(path, params)` method.
        q: search query string
        limit: maximum number of items to return overall (best-effort)
        offset: offset into the aggregated results (best-effort)
        object_type: optional specific object type key (e.g. 'dcim.sites') to limit the search

    Returns:
        A dict with keys: total (int), results (list of items with additional metadata)
    """
    endpoints = {}
    if object_type:
        if object_type not in NETBOX_OBJECT_TYPES:
            raise ValueError(f"unknown object_type: {object_type}")
        endpoints[object_type] = NETBOX_OBJECT_TYPES[object_type]
    else:
        endpoints = NETBOX_OBJECT_TYPES.copy()

    aggregated: List[Dict[str, Any]] = []
    total = 0

    for obj_type, endpoint in endpoints.items():
        path = f"/{endpoint}/"
        params = {"q": q, "limit": limit, "offset": 0}
        try:
            resp = client.get(path, params=params)
        except Exception:
            # Ignore errors for individual endpoints but continue searching others
            continue

        try:
            data = resp.json()
        except Exception:
            continue

        results = data.get("results") or []
        count = data.get("count") or len(results)
        total += count

        # Annotate each result with object_type for downstream consumers
        for item in results:
            annotated = dict(item)
            annotated["_mcp_object_type"] = obj_type
            aggregated.append(annotated)

        # simple stop condition if we've accumulated enough
        if len(aggregated) >= (offset + limit):
            break

    # apply offset and limit to aggregated results
    sliced = aggregated[offset: offset + limit]

    return {"total": total, "results": sliced}

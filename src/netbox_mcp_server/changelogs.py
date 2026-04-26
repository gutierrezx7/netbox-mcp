"""Changelogs retrieval utilities for NetBox MCP.

Provides netbox_get_changelogs which queries the NetBox changelog endpoint with
filters and pagination.
"""
from typing import Dict, Any, Optional

from .types import NETBOX_OBJECT_TYPES


def netbox_get_changelogs(client, filters: Optional[Dict[str, Any]] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """Retrieve changelogs with optional filters and pagination.

    Args:
        client: NetBoxRestClient-like instance
        filters: query filters (passed as params)
        limit: pagination limit
        offset: pagination offset
    """
    path = "/extras/changelogentries/"
    params = {}
    if filters:
        params.update(filters)
    params.update({"limit": limit, "offset": offset})

    resp = client.get(path, params=params)
    try:
        return resp.json()
    except Exception:
        raise

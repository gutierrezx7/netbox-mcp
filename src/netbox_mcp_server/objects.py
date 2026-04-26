"""Objects listing utilities for NetBox MCP.

Provides netbox_get_objects which lists objects for a specific NetBox
object type, applies filters (validated), and returns paginated results.
"""
from typing import Dict, Any, Optional

from .types import NETBOX_OBJECT_TYPES
from .validators import parse_lookup_expressions


def netbox_get_objects(client, object_type: str, filters: Optional[Dict[str, Any]] = None, limit: int = 50, offset: int = 0, fields: Optional[str] = None) -> Dict[str, Any]:
    """List objects for a given object_type with filters and pagination.

    Args:
        client: NetBoxRestClient-like instance with .get(path, params)
        object_type: key from NETBOX_OBJECT_TYPES map (e.g., 'dcim.sites')
        filters: dict of filters (lookup expressions) to validate and pass as query params
        limit: number of items to return
        offset: starting offset
        fields: comma-separated string of fields to include

    Returns:
        dict with keys 'count' and 'results' as returned by NetBox API
    """
    if object_type not in NETBOX_OBJECT_TYPES:
        raise ValueError(f"unknown object_type: {object_type}")

    endpoint = NETBOX_OBJECT_TYPES[object_type]
    path = f"/{endpoint}/"

    params = {}
    if filters:
        # validate filters
        parse_lookup_expressions(filters)
        # merge filters into params
        params.update(filters)

    params.update({"limit": limit, "offset": offset})
    if fields:
        params["fields"] = fields

    resp = client.get(path, params=params)
    try:
        return resp.json()
    except Exception:
        raise


def get_object_by_id(client, object_type: str, obj_id: int, fields: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve a single object by its ID with optional field filtering.

    Args:
        client: NetBoxRestClient-like instance with .get(path, params)
        object_type: key from NETBOX_OBJECT_TYPES map (e.g., 'dcim.sites')
        obj_id: numeric identifier of the object
        fields: optional comma-separated list of fields to return

    Returns:
        The JSON-decoded object dict as returned by NetBox.
    """
    if object_type not in NETBOX_OBJECT_TYPES:
        raise ValueError(f"unknown object_type: {object_type}")

    endpoint = NETBOX_OBJECT_TYPES[object_type]
    path = f"/{endpoint}{obj_id}/"
    params = {}
    if fields:
        params["fields"] = fields

    resp = client.get(path, params=params)
    try:
        return resp.json()
    except Exception:
        raise

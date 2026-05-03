"""FastMCP server for NetBox MCP - registers all 7 tools.

Each tool captures the NetBoxRestClient via closure, so the client
is injected transparently without being exposed as a tool parameter.
"""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from netbox_mcp_server import changelogs, crud, objects, search

mcp = FastMCP("netbox-mcp")


def register_tools(client: Any) -> None:
    """Register all NetBox MCP tools on the FastMCP instance.

    Args:
        client: A NetBoxRestClient instance used to communicate with the NetBox API.
    """

    def _netbox_search_objects(
        q: str,
        limit: int = 50,
        offset: int = 0,
        object_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search across NetBox object endpoints."""
        return search.netbox_search_objects(
            client, q=q, limit=limit, offset=offset, object_type=object_type
        )

    mcp.add_tool(_netbox_search_objects, name="netbox_search_objects")

    def _netbox_get_objects(
        object_type: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List objects for a given object_type with filters and pagination."""
        return objects.netbox_get_objects(
            client,
            object_type=object_type,
            filters=filters,
            limit=limit,
            offset=offset,
            fields=fields,
        )

    mcp.add_tool(_netbox_get_objects, name="netbox_get_objects")

    def _netbox_get_object_by_id(
        object_type: str,
        obj_id: int,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve a single object by its ID."""
        return objects.get_object_by_id(
            client, object_type=object_type, obj_id=obj_id, fields=fields
        )

    mcp.add_tool(_netbox_get_object_by_id, name="netbox_get_object_by_id")

    def _netbox_create_object(
        object_type: str,
        payload: Any,
    ) -> Dict[str, Any]:
        """Create single or bulk objects."""
        return crud.netbox_create_object(
            client, object_type=object_type, payload=payload
        )

    mcp.add_tool(_netbox_create_object, name="netbox_create_object")

    def _netbox_update_object(
        object_type: str,
        payload: Any,
    ) -> Dict[str, Any]:
        """Update single or bulk objects."""
        return crud.netbox_update_object(
            client, object_type=object_type, payload=payload
        )

    mcp.add_tool(_netbox_update_object, name="netbox_update_object")

    def _netbox_delete_object(
        object_type: str,
        ids: Any,
    ) -> Dict[str, Any]:
        """Delete single or multiple objects."""
        return crud.netbox_delete_object(
            client, object_type=object_type, ids=ids
        )

    mcp.add_tool(_netbox_delete_object, name="netbox_delete_object")

    def _netbox_get_changelogs(
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Retrieve changelogs with optional filters and pagination."""
        return changelogs.netbox_get_changelogs(
            client, filters=filters, limit=limit, offset=offset
        )

    mcp.add_tool(_netbox_get_changelogs, name="netbox_get_changelogs")

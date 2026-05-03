"""FastMCP server for NetBox MCP - registers all 7 tools."""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from netbox_mcp_server import changelogs, crud, objects, search

_client: Any = None
mcp = FastMCP("netbox-mcp")


def set_client(client: Any) -> None:
    global _client
    _client = client


@mcp.tool()
def netbox_search_objects(q: str, limit: int = 50, offset: int = 0, object_type: Optional[str] = None) -> Dict[str, Any]:
    return search.netbox_search_objects(_client, q=q, limit=limit, offset=offset, object_type=object_type)


@mcp.tool()
def netbox_get_objects(object_type: str, filters: Optional[Dict[str, Any]] = None, limit: int = 50, offset: int = 0, fields: Optional[str] = None) -> Dict[str, Any]:
    return objects.netbox_get_objects(_client, object_type=object_type, filters=filters, limit=limit, offset=offset, fields=fields)


@mcp.tool()
def netbox_get_object_by_id(object_type: str, obj_id: int, fields: Optional[str] = None) -> Dict[str, Any]:
    return objects.get_object_by_id(_client, object_type=object_type, obj_id=obj_id, fields=fields)


@mcp.tool()
def netbox_create_object(object_type: str, payload: Any) -> Dict[str, Any]:
    return crud.netbox_create_object(_client, object_type=object_type, payload=payload)


@mcp.tool()
def netbox_update_object(object_type: str, payload: Any) -> Dict[str, Any]:
    return crud.netbox_update_object(_client, object_type=object_type, payload=payload)


@mcp.tool()
def netbox_delete_object(object_type: str, ids: Any) -> Dict[str, Any]:
    return crud.netbox_delete_object(_client, object_type=object_type, ids=ids)


@mcp.tool()
def netbox_get_changelogs(filters: Optional[Dict[str, Any]] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    return changelogs.netbox_get_changelogs(_client, filters=filters, limit=limit, offset=offset)


def register_tools(client: Any) -> None:
    set_client(client)

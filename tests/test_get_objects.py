from unittest.mock import MagicMock

from netbox_mcp_server.objects import netbox_get_objects


def test_netbox_get_objects_calls_client_and_returns_json():
    client = MagicMock()
    resp = MagicMock()
    resp.json.return_value = {"count": 1, "results": [{"id": 1}]}
    client.get.return_value = resp

    result = netbox_get_objects(client, object_type="dcim.sites", filters={"name": "A"}, limit=10, offset=0)

    assert result["count"] == 1
    assert isinstance(result["results"], list)
    client.get.assert_called_once()

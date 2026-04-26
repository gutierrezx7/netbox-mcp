from unittest.mock import MagicMock

from netbox_mcp_server.crud import netbox_create_object


def test_netbox_create_object_single():
    client = MagicMock()
    resp = MagicMock()
    resp.json.return_value = {"id": 1}
    client.post.return_value = resp

    payload = {"name": "Site A"}
    result = netbox_create_object(client, object_type="dcim.sites", payload=payload)

    assert result["id"] == 1
    client.post.assert_called_once()


def test_netbox_create_object_bulk():
    client = MagicMock()
    resp = MagicMock()
    resp.json.return_value = [{"id": 1}, {"id": 2}]
    client.post.return_value = resp

    payload = [{"name": "A"}, {"name": "B"}]
    result = netbox_create_object(client, object_type="dcim.sites", payload=payload)

    assert "bulk_results" in result
    client.post.assert_called()

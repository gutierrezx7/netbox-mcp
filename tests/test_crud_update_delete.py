from unittest.mock import MagicMock

from netbox_mcp_server.crud import netbox_update_object, netbox_delete_object


def test_netbox_update_object_single():
    client = MagicMock()
    resp = MagicMock()
    resp.json.return_value = {"id": 1, "name": "Updated"}
    client.request.return_value = resp

    payload = {"id": 1, "name": "Updated"}
    result = netbox_update_object(client, object_type="dcim.sites", payload=payload)

    assert result["id"] == 1
    client.request.assert_called()


def test_netbox_delete_object_single_and_bulk():
    client = MagicMock()
    resp = MagicMock()
    resp.status_code = 204
    client.request.return_value = resp

    single = netbox_delete_object(client, object_type="dcim.sites", ids=1)
    assert single["id"] == 1

    bulk = netbox_delete_object(client, object_type="dcim.sites", ids=[1, 2])
    assert "deleted" in bulk
    assert len(bulk["deleted"]) == 2

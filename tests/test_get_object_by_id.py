from unittest.mock import MagicMock

from netbox_mcp_server.objects import get_object_by_id


def test_get_object_by_id_returns_json():
    client = MagicMock()
    resp = MagicMock()
    resp.json.return_value = {"id": 42, "name": "Example"}
    client.get.return_value = resp

    result = get_object_by_id(client, object_type="dcim.sites", obj_id=42, fields="id,name")

    assert result["id"] == 42
    client.get.assert_called_once()

from unittest.mock import MagicMock

from netbox_mcp_server.changelogs import netbox_get_changelogs


def test_netbox_get_changelogs_basic():
    client = MagicMock()
    resp = MagicMock()
    resp.json.return_value = {"count": 0, "results": []}
    client.get.return_value = resp

    result = netbox_get_changelogs(client, filters={"user": "admin"}, limit=10, offset=0)

    assert "results" in result
    client.get.assert_called_once()

import pytest
from unittest.mock import MagicMock, PropertyMock

from netbox_mcp_server.search import netbox_search_objects


def test_netbox_search_objects_aggregates_results():
    client = MagicMock()

    # Mock response objects with .json()
    resp_sites = MagicMock()
    resp_sites.json.return_value = {"count": 1, "results": [{"id": 1, "name": "Site A"}]}

    resp_devices = MagicMock()
    resp_devices.json.return_value = {"count": 1, "results": [{"id": 2, "name": "Device X"}]}

    # The new implementation uses client.session.get() to bypass rate limiting
    def session_get_side_effect(url, params=None, timeout=None, verify=None):
        if "/dcim/sites/" in url:
            return resp_sites
        if "/dcim/devices/" in url:
            return resp_devices
        raise RuntimeError(f"unexpected url: {url}")

    client.base_url = "http://netbox.example.com"
    client.timeout = 30
    client.ssl_verify = True
    client.session = MagicMock()
    client.session.get.side_effect = session_get_side_effect

    result = netbox_search_objects(client, q="test", limit=10)

    assert result["total"] >= 0
    assert isinstance(result["results"], list)
    # The annotated object types should be present in results
    for item in result["results"]:
        assert "_mcp_object_type" in item

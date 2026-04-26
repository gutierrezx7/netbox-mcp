import pytest

from src.netbox_mcp_server.types import NETBOX_OBJECT_TYPES

def test_netbox_object_types_structure():
    """
    Verify the structure and key entries of NETBOX_OBJECT_TYPES.
    """
    assert isinstance(NETBOX_OBJECT_TYPES, dict)

    # Check for presence of key expected types across different modules
    expected_keys = {
        "dcim.sites",
        "dcim.devices",
        "ipam.ip-addresses",
        "ipam.prefixes",
        "circuits.circuits",
        "tenancy.tenants",
        "virtualization.virtual-machines",
        "extras.tags",
        "wireless.wireless-lans",
    }
    for key in expected_keys:
        assert key in NETBOX_OBJECT_TYPES, f"Missing expected key: {key}"

    # Check for correct endpoint path format for a few examples
    assert NETBOX_OBJECT_TYPES["dcim.sites"] == "dcim/sites"
    assert NETBOX_OBJECT_TYPES["ipam.prefixes"] == "ipam/prefixes"
    assert NETBOX_OBJECT_TYPES["virtualization.virtual-machines"] == "virtualization/virtual-machines"
    assert NETBOX_OBJECT_TYPES["extras.tags"] == "extras/tags"

    # Ensure no empty endpoint paths
    for obj_type, endpoint in NETBOX_OBJECT_TYPES.items():
        assert endpoint, f"Endpoint path for {obj_type} is empty"
        assert "/" in endpoint, f"Endpoint path for {obj_type} does not contain a slash: {endpoint}"


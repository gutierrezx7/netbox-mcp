import pytest

from netbox_mcp_server.validators import validate_object_type, parse_lookup_expressions
from netbox_mcp_server.types import NETBOX_OBJECT_TYPES


def test_validate_object_type_positive():
    # pick a key that should exist (from types)
    any_key = next(iter(NETBOX_OBJECT_TYPES.keys()))
    assert validate_object_type(any_key) is True


def test_validate_object_type_negative():
    assert validate_object_type("nonexistent.object") is False


def test_parse_lookup_expressions_valid():
    filters = {
        "name__icontains": "example",
        "id__in": [1, 2, 3],
        "status": "active",
    }
    assert parse_lookup_expressions(filters) is filters


def test_parse_lookup_expressions_invalid_lookup():
    with pytest.raises(ValueError):
        parse_lookup_expressions({"name__badlookup": "x"})


def test_parse_lookup_expressions_string_too_long():
    long_string = "x" * 1001
    with pytest.raises(ValueError):
        parse_lookup_expressions({"note": long_string})

"""Validation utilities for NetBox MCP server.

Provides functions to validate object types against the allowlist coming from
`netbox_mcp_server.types.NETBOX_OBJECT_TYPES` and to sanitize / validate filter
lookup expressions used by the MCP tools.

The functions are intentionally small and dependency-free so they are easy to
unit-test and reason about.
"""
from typing import Dict, Any

from .types import NETBOX_OBJECT_TYPES

# Allowed lookup suffixes (NetBox/Django-style lookups)
ALLOWED_LOOKUPS = {
    "in",
    "exact",
    "iexact",
    "contains",
    "icontains",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "lt",
    "lte",
    "gt",
    "gte",
}

# Maximum allowed length for string inputs (guardrail)
MAX_STRING_LENGTH = 500


def validate_object_type(obj_type: str) -> bool:
    """Return True if obj_type is allowed (present in NETBOX_OBJECT_TYPES).

    The obj_type should match keys in NETBOX_OBJECT_TYPES, e.g. 'dcim.sites'.
    """
    return obj_type in NETBOX_OBJECT_TYPES


def parse_lookup_expressions(filters: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize lookup expressions in the given filters dict.

    Rules enforced:
    - Keys may be of the form "field" or "field__lookup" where "lookup" is
      one of the ALLOWED_LOOKUPS set.
    - String values are limited to MAX_STRING_LENGTH characters.
    - If any check fails, ValueError is raised.

    Returns the original dict (not a deep copy) when validation passes.
    """
    if not isinstance(filters, dict):
        raise ValueError("filters must be a dict")

    for key, value in filters.items():
        if not isinstance(key, str) or key == "":
            raise ValueError(f"invalid filter key: {key!r}")

        # split lookup suffix if present
        parts = key.split("__")
        if len(parts) > 1:
            lookup = parts[-1]
            if lookup not in ALLOWED_LOOKUPS:
                raise ValueError(f"disallowed lookup '{lookup}' in filter key '{key}'")

        # validate value types and lengths
        if isinstance(value, str):
            if len(value) > MAX_STRING_LENGTH:
                raise ValueError(f"string value for '{key}' exceeds max length {MAX_STRING_LENGTH}")
        elif isinstance(value, (list, tuple)):
            # For list-like values, ensure each string element meets length constraints
            for item in value:
                if isinstance(item, str) and len(item) > MAX_STRING_LENGTH:
                    raise ValueError(f"string element in '{key}' exceeds max length {MAX_STRING_LENGTH}")
        # other types (int, bool, None, dict) are accepted as-is

    return filters

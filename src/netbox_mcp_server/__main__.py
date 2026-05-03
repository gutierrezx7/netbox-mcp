"""Entry point for the NetBox MCP server.

Usage:
    python3 -m netbox_mcp_server
    python3 -m netbox_mcp_server --transport=sse
    python3 -m netbox_mcp_server --transport=stdio --netbox-url=https://netbox.example.com --netbox-token=xxx
"""

import argparse
import sys

from netbox_mcp_server.client import NetBoxRestClient
from netbox_mcp_server.config import get_settings
from netbox_mcp_server.server import mcp, register_tools


def main() -> None:
    transport_parser = argparse.ArgumentParser(add_help=False)
    transport_parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "sse", "streamable-http"],
    )
    transport_args, remaining = transport_parser.parse_known_args()

    settings = get_settings(cli_args=tuple(remaining) if remaining else None)

    client = NetBoxRestClient(
        base_url=settings.NETBOX_URL,
        token=settings.NETBOX_TOKEN,
        timeout=settings.TIMEOUT,
        rate_limit=settings.RATE_LIMIT,
    )

    register_tools(client)

    mcp.run(transport=transport_args.transport)


if __name__ == "__main__":
    main()

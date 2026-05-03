"""Entry point for the NetBox MCP server.

Usage:
    python3 -m netbox_mcp_server
    python3 -m netbox_mcp_server --transport=sse --host=0.0.0.0 --port=8004
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
    transport_parser.add_argument("--host", default=None)
    transport_parser.add_argument("--port", type=int, default=None)
    transport_args, remaining = transport_parser.parse_known_args()

    settings = get_settings(cli_args=tuple(remaining) if remaining else None)

    client = NetBoxRestClient(
        base_url=settings.NETBOX_URL,
        token=settings.NETBOX_TOKEN,
        timeout=settings.TIMEOUT,
        rate_limit=settings.RATE_LIMIT,
    )

    register_tools(client)

    run_kwargs = {"transport": transport_args.transport}
    if transport_args.host:
        run_kwargs["host"] = transport_args.host
    if transport_args.port:
        run_kwargs["port"] = transport_args.port

    mcp.run(**run_kwargs)


if __name__ == "__main__":
    main()

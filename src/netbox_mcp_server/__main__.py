import argparse

from netbox_mcp_server.client import NetBoxRestClient
from netbox_mcp_server.config import get_settings
from netbox_mcp_server.server import mcp, register_tools


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse", "streamable-http"])
    transport_args, remaining = parser.parse_known_args()

    settings = get_settings(cli_args=tuple(remaining) if remaining else None)

    client = NetBoxRestClient(
        base_url=settings.NETBOX_URL,
        token=settings.NETBOX_TOKEN,
        timeout=settings.TIMEOUT,
        rate_limit=settings.RATE_LIMIT,
        ssl_verify=settings.NETBOX_SSL_VERIFY,
    )

    register_tools(client)

    tools = mcp._tool_manager.list_tools()
    for t in tools:
        import sys
        print(f"Registered: {t.name}", file=sys.stderr)

    mcp.run(transport=transport_args.transport)


if __name__ == "__main__":
    main()

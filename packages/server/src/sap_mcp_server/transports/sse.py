"""SSE-based MCP Server implementation (Future)"""

import logging

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for SSE MCP server

    Note: SSE (Server-Sent Events) transport is not yet implemented.
    This is a placeholder for future implementation.

    SSE transport will enable:
    - Browser-based MCP clients
    - Real-time streaming updates
    - HTTP/HTTPS communication
    - WebSocket-like functionality over HTTP
    """
    raise NotImplementedError(
        "SSE transport is not yet implemented. Use stdio transport instead:\n"
        "  python -m sap_mcp_server.transports.stdio\n"
        "or:\n"
        "  sap-mcp-server-stdio"
    )


if __name__ == "__main__":
    import asyncio

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    try:
        asyncio.run(main())
    except NotImplementedError as e:
        logger.error(str(e))
        exit(1)

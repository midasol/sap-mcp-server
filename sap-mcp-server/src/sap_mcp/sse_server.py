"""SSE-based MCP Server implementation for remote connections"""

import asyncio
import logging
from pathlib import Path

from dotenv import load_dotenv
from mcp import types
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

from .protocol.tools import tool_registry
from .sap import tools as _  # noqa: F401  # Import to trigger tool registration

logger = logging.getLogger(__name__)


async def handle_sse(request):
    """Handle SSE connection from MCP clients"""
    async with SseServerTransport("/messages") as (read_stream, write_stream):
        # Create MCP server instance
        server = Server("sap-mcp")

        # Register tools
        @server.list_tools()
        async def list_tools() -> list[types.Tool]:
            """List all available tools"""
            tool_list = tool_registry.list_tools()
            return [
                types.Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=tool.inputSchema,
                )
                for tool in tool_list
            ]

        @server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
            """Call a tool with the given arguments"""
            from .protocol.schemas import ToolCallRequest

            try:
                # Create tool call request
                request = ToolCallRequest(name=name, arguments=arguments)

                # Call the tool
                result = await tool_registry.call_tool(request)

                # Return result as text content
                return [types.TextContent(type="text", text=str(result.content))]
            except Exception as e:
                logger.error(f"Tool call failed: {e}", exc_info=True)
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

        # Run the server
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


async def main() -> None:
    """Main entry point for SSE MCP server"""

    # Load environment variables from .env.server file
    env_path = Path(__file__).parent.parent.parent / ".env.server"
    if not env_path.exists():
        # Fallback to .env for backward compatibility
        env_path = Path(__file__).parent.parent.parent / ".env"

    load_dotenv(dotenv_path=env_path)
    logger.info(f"Loaded server environment variables from {env_path}")

    # Get server configuration from environment
    import os

    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))

    # Create Starlette app
    app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
        ],
    )

    # Run server with uvicorn
    import uvicorn

    logger.info(f"Starting SAP MCP SSE server on {host}:{port}")
    logger.info(f"SSE endpoint: http://{host}:{port}/sse")

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

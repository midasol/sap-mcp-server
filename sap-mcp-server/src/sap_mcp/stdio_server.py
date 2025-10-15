"""Stdio-based MCP Server implementation"""

import asyncio
import logging
from pathlib import Path

from dotenv import load_dotenv
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .protocol.tools import tool_registry
from .sap import tools as _  # noqa: F401  # Import to trigger tool registration

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for stdio MCP server"""

    # Load environment variables from .env.server file
    # Search in multiple locations to handle different installation methods
    env_paths = [
        Path.cwd() / ".env.server",  # Current working directory
        Path.cwd() / "sap-mcp-server" / ".env.server",  # If running from project root
        Path(__file__).parent.parent.parent / ".env.server",  # Relative to source
        Path.home() / ".env.server",  # User home directory
    ]
    
    env_path = None
    for path in env_paths:
        if path.exists():
            env_path = path
            break
    
    if env_path is None:
        # Fallback to .env for backward compatibility
        env_path = Path.cwd() / ".env"
        if not env_path.exists():
            logger.warning("No .env.server or .env file found in any expected location")
            logger.warning(f"Searched locations: {[str(p) for p in env_paths]}")

    load_dotenv(dotenv_path=env_path)
    logger.info(f"Loaded server environment variables from {env_path}")

    # Create MCP server
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
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

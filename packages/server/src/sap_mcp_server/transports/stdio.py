"""Stdio-based MCP Server implementation"""

import asyncio
import logging
from pathlib import Path

from dotenv import load_dotenv
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from sap_mcp_server.tools import tool_registry
from sap_mcp_server.protocol.schemas import ToolCallRequest

logger = logging.getLogger(__name__)


def find_env_file() -> Path | None:
    """Find .env.server file in multiple possible locations"""
    env_paths = [
        Path.cwd() / ".env.server",  # Current working directory
        Path.cwd() / "sap-mcp-server" / ".env.server",  # If running from project root
        Path(__file__).parent.parent.parent.parent.parent.parent / ".env.server",  # Project root
        Path.home() / ".env.server",  # User home directory
    ]

    for path in env_paths:
        if path.exists():
            return path

    # Fallback to .env for backward compatibility
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        return env_path

    logger.warning("No .env.server or .env file found in any expected location")
    logger.warning(f"Searched locations: {[str(p) for p in env_paths]}")
    return None


async def main() -> None:
    """Main entry point for stdio MCP server"""

    # Load environment variables
    env_path = find_env_file()
    if env_path:
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded server environment variables from {env_path}")
    else:
        logger.warning("Starting server without environment file")

    # Create MCP server
    server = Server("sap-mcp")

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
    logger.info("Starting SAP MCP stdio server...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    asyncio.run(main())

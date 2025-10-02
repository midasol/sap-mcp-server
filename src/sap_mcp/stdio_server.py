"""Stdio-based MCP Server implementation"""

import asyncio
import logging

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .protocol.tools import tool_registry
from .sap import tools as _  # noqa: F401  # Import to trigger tool registration

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for stdio MCP server"""

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

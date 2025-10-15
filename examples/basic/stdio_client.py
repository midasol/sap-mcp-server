"""
Stdio-based MCP Client - Auto-spawns server process

This client automatically starts the SAP MCP server as a subprocess.
The server package must be installed for this to work.

Prerequisites:
    pip install -e ../../packages/server

For connecting to a separately running server, use sse_client.py instead.
"""

import asyncio
import json
import sys
from typing import Any, Dict

from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


def format_response(result: Any) -> Dict[str, Any]:
    """Parse and format MCP tool response"""
    if not result.content or len(result.content) == 0:
        return {"error": "Empty response"}

    content_item = result.content[0]
    if not hasattr(content_item, "text"):
        return {"error": "No text content"}

    try:
        import ast

        response_data = ast.literal_eval(content_item.text)

        # Extract actual data from nested structure
        if isinstance(response_data, list) and len(response_data) > 0:
            actual_response = response_data[0]
            if "text" in actual_response:
                return ast.literal_eval(actual_response["text"])

        return response_data

    except (ValueError, SyntaxError) as e:
        return {"error": f"Parse error: {e}", "raw": content_item.text}


async def main() -> None:
    """Main test function"""
    print("\n🚀 SAP MCP Client - Stdio Mode")
    print("=" * 60)
    print("This client auto-spawns the server as a subprocess")
    print("=" * 60)

    # Server will be spawned as a subprocess
    server_params = StdioServerParameters(
        command="python", args=["-m", "sap_mcp_server.transports.stdio"]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                print("\n📡 Initializing MCP session...")
                await session.initialize()
                print("✅ Session initialized")

                # Authenticate with SAP
                print("\n=== SAP Authentication ===")
                auth_result = await session.call_tool("sap_authenticate", {})
                auth_response = format_response(auth_result)

                if auth_response.get("success"):
                    print("✅ Authentication successful")
                else:
                    print(f"❌ Authentication failed: {auth_response.get('error')}")
                    print("Please check SAP credentials in server's .env file")
                    return

                # Get specific entity by OrderID
                print("\n=== Get Entity (OrderID: 91000092) ===")
                entity_result = await session.call_tool(
                    "sap_get_entity",
                    {
                        "service": "Z_SALES_ORDER_GENAI_SRV",
                        "entity_set": "zsd004Set",
                        "entity_key": "91000092",
                    },
                )

                entity_response = format_response(entity_result)

                if entity_response.get("success"):
                    print("✅ Entity retrieved successfully")
                    if "data" in entity_response:
                        print(
                            json.dumps(
                                entity_response["data"], indent=2, ensure_ascii=False
                            )
                        )
                else:
                    print(f"❌ Failed: {entity_response.get('error')}")

                print("\n✅ Test completed")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(
            "\nTroubleshooting:"
        )
        print("1. Is the server package installed? Run: pip install -e ../../packages/server")
        print("2. Can you run the server manually? Try: python -m sap_mcp_server.transports.stdio")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

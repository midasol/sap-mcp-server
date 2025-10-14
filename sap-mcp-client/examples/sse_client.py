"""SSE-based MCP Client test - connects to remote SAP MCP server"""

import asyncio
import json

from mcp import ClientSession
from mcp.client.sse import sse_client


async def main() -> None:
    """Test SAP MCP client connecting to SSE server"""

    # SSE server URL (update based on deployment)
    # Development: http://localhost:8000/sse
    # Production: http://sap-mcp-server.company.com/sse
    server_url = "http://localhost:8000/sse"

    print(f"Connecting to SAP MCP server at {server_url}...")

    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            print("✅ Connected to SAP MCP server")

            # Authenticate with SAP (credentials loaded from server environment)
            print("\n=== Authenticating with SAP ===")
            auth_result = await session.call_tool("sap_authenticate", {})
            print(f"Auth result: {auth_result}")

            # Get specific entity by OrderID
            print("\n=== Fetching Entity (OrderID: 91000092) ===")
            entity_result = await session.call_tool(
                "sap_get_entity",
                {
                    "service": "Z_SALES_ORDER_GENAI_SRV",
                    "entity_set": "zsd004Set",
                    "entity_key": "91000092",
                },
            )

            # Extract and format the JSON response
            if entity_result.content and len(entity_result.content) > 0:
                content_item = entity_result.content[0]
                if hasattr(content_item, "text"):
                    import ast

                    try:
                        # Parse the MCP response wrapper
                        response_data = ast.literal_eval(content_item.text)

                        # Extract actual data
                        if isinstance(response_data, list) and len(response_data) > 0:
                            actual_response = response_data[0]
                            if "text" in actual_response:
                                actual_data = ast.literal_eval(actual_response["text"])
                                if "data" in actual_data:
                                    print(
                                        json.dumps(
                                            actual_data["data"],
                                            indent=2,
                                            ensure_ascii=False,
                                        )
                                    )
                                else:
                                    print(
                                        json.dumps(
                                            actual_data, indent=2, ensure_ascii=False
                                        )
                                    )
                        elif "data" in response_data:
                            print(
                                json.dumps(
                                    response_data["data"], indent=2, ensure_ascii=False
                                )
                            )
                        else:
                            print(
                                json.dumps(response_data, indent=2, ensure_ascii=False)
                            )
                    except (ValueError, SyntaxError) as e:
                        print(f"Error parsing response: {e}")
                        print(content_item.text)
            else:
                print(f"{entity_result}")

            print("\n✅ Test completed successfully")


if __name__ == "__main__":
    asyncio.run(main())

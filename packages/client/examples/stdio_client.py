import asyncio
import json

from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


async def main() -> None:
    # Connect to the MCP server via stdio
    server_params = StdioServerParameters(
        command="python", args=["-m", "sap_mcp_server.transports.stdio"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Authenticate with SAP (credentials loaded from environment variables)
            auth_result = await session.call_tool("sap_authenticate", {})
            print(f"Auth result: {auth_result}")

            # Get specific entity by OrderID
            entity_result = await session.call_tool(
                "sap_get_entity",
                {
                    "service": "Z_SALES_ORDER_GENAI_SRV",
                    "entity_set": "zsd004Set",
                    "entity_key": "91000092",
                },
            )

            # Extract and format the JSON response
            print("\n=== Entity Result (OrderID: 91000092) ===")
            if entity_result.content and len(entity_result.content) > 0:
                # Get the first content item (text response)
                content_item = entity_result.content[0]
                if hasattr(content_item, "text"):
                    # The MCP response wraps the tool result in a string format
                    # Parse it using ast.literal_eval first to handle single quotes
                    import ast

                    try:
                        # Try to evaluate the string as Python literal
                        response_data = ast.literal_eval(content_item.text)
                        # Pretty print the data field which contains the entity
                        if isinstance(response_data, list) and len(response_data) > 0:
                            # Extract the actual response from the MCP wrapper
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
                        # If parsing fails, print the raw response
                        print(f"Error parsing response: {e}")
                        print(content_item.text)
            else:
                print(f"{entity_result}")


if __name__ == "__main__":
    asyncio.run(main())

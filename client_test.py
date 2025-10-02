import asyncio

from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


async def main() -> None:
    # Connect to the MCP server via stdio
    server_params = StdioServerParameters(
        command="python", args=["-m", "sap_mcp.stdio_server"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Authenticate with SAP
            auth_result = await session.call_tool(
                "sap_authenticate",
                {
                    "host": "34.64.166.83",
                    "username": "admin",
                    "password": "Ahfelqm2@13",
                },
            )
            print(f"Auth result: {auth_result}")

            # Query SAP data
            result = await session.call_tool(
                "sap_query",
                {
                    "service": "Z_SALES_ORDER_GENAI_SRV",
                    "entity_set": "zsd004Set",
                    "filter": "Auart eq 'OR'",
                },
            )

            print(f"Query result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

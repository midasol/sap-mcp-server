"""AI Order Inquiry Chatbot

This chatbot uses Gemini AI to extract order IDs from natural language queries
and retrieves order information from SAP Gateway using MCP.

Example queries:
- "Show me information for order 91000092"
- "Can you check order 91000092?"
- "What's the status of order 91000092?"
- "Order number 91000092 details please"
"""

import ast
import asyncio
import os
from typing import Any, Dict, Optional

from google import genai
from google.genai import types
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


class OrderInquiryChatbot:
    """AI-powered chatbot for SAP order inquiries"""

    def __init__(self, gemini_api_key: str, sap_config: Dict[str, str]):
        """Initialize the chatbot

        Args:
            gemini_api_key: Google Gemini API key
            sap_config: SAP business configuration (credentials loaded from .env.server)
                - service: OData service name
                - entity_set: Entity set name
        """
        self.gemini_client = genai.Client(api_key=gemini_api_key)
        self.sap_config = sap_config
        self.gemini_model = "gemini-flash-latest"

    def extract_order_id(self, user_query: str) -> Optional[str]:
        """Extract order ID from natural language query using Gemini

        Args:
            user_query: User's natural language query

        Returns:
            Extracted order ID or None if not found
        """
        print(f"\n🤔 Analyzing query: '{user_query}'")

        system_instruction = """You are an order ID extraction assistant.
Extract the order ID from the user's query.

Rules:
1. Order IDs are typically 8-digit numbers (e.g., 91000092)
2. Return ONLY the order ID number, nothing else
3. If no order ID is found, return "NONE"
4. Do not add any explanation or additional text

Examples:
- "Show me order 91000092" → 91000092
- "Can you check order 91000092?" → 91000092
- "What's the status of 91000092?" → 91000092
- "Order number 91000092 details" → 91000092
- "Show me order information" → NONE
"""

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_query)],
            ),
        ]

        config = types.GenerateContentConfig(
            temperature=0,
            system_instruction=[types.Part.from_text(text=system_instruction)],
        )

        try:
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=contents,
                config=config,
            )

            order_id = response.text.strip()

            # Clean up the response
            if order_id.upper() == "NONE" or not order_id:
                print("❌ No order ID found in query")
                return None

            # Validate it's a number
            if not order_id.isdigit():
                print(f"⚠️  Extracted value is not a valid order ID: {order_id}")
                return None

            print(f"✅ Extracted Order ID: {order_id}")
            return order_id

        except Exception as e:
            print(f"❌ Error extracting order ID: {e}")
            return None

    async def get_order_info(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve order information from SAP using MCP

        Args:
            order_id: SAP order ID

        Returns:
            Order data dictionary or None if error
        """
        print("\n📡 Retrieving order information from SAP...")

        server_params = StdioServerParameters(
            command="python", args=["-m", "sap_mcp_server.transports.stdio"]
        )

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()

                    # Authenticate with SAP (credentials from .env.server)
                    auth_result = await session.call_tool("sap_authenticate", {})

                    # Check authentication
                    if not auth_result or not auth_result.content:
                        print("❌ SAP authentication failed")
                        return None

                    # Get entity by OrderID (only business parameters)
                    entity_result = await session.call_tool(
                        "sap_get_entity",
                        {
                            "service": self.sap_config["service"],
                            "entity_set": self.sap_config["entity_set"],
                            "entity_key": order_id,
                        },
                    )

                    # Parse the MCP response
                    if entity_result.content and len(entity_result.content) > 0:
                        content_item = entity_result.content[0]
                        if hasattr(content_item, "text"):
                            try:
                                response_data = ast.literal_eval(content_item.text)
                                if (
                                    isinstance(response_data, list)
                                    and len(response_data) > 0
                                ):
                                    actual_response = response_data[0]
                                    if "text" in actual_response:
                                        actual_data = ast.literal_eval(
                                            actual_response["text"]
                                        )
                                        if "data" in actual_data:
                                            print(
                                                "✅ Order data retrieved successfully"
                                            )
                                            return actual_data["data"]
                            except (ValueError, SyntaxError) as e:
                                print(f"❌ Error parsing response: {e}")
                                return None

                    print("❌ No order data found")
                    return None

        except Exception as e:
            print(f"❌ Error retrieving order: {e}")
            return None

    def format_order_response(
        self, order_data: Dict[str, Any], requested_order_id: str
    ) -> str:
        """Format order data into user-friendly response

        Args:
            order_data: SAP order data dictionary
            requested_order_id: The order ID that was requested

        Returns:
            Formatted response string
        """
        if not order_data or "d" not in order_data:
            return "❌ Order information not found."

        order = order_data["d"]
        returned_order_id = order.get("OrderId", "")

        # Check if returned order ID matches requested order ID
        mismatch_warning = ""
        if returned_order_id and returned_order_id != requested_order_id:
            mismatch_warning = f"""
⚠️  WARNING: Order ID Mismatch!
   Requested: {requested_order_id}
   Returned: {returned_order_id}

   The requested order may not exist. Showing available order instead.

"""

        response = f"""
{mismatch_warning}📦 Order Information
{'=' * 50}

🔢 Order ID: {returned_order_id or 'N/A'}
📝 Customer PO Number: {order.get('Bstnk', 'N/A')}
📋 Order Type: {order.get('Auart', 'N/A')}

👤 Customer Information
   Customer Number: {order.get('Kunnr', 'N/A')}

📦 Item Information
   Material Number: {order.get('Matnr', 'N/A')}
   Order Quantity: {order.get('Wmeng', 'N/A')}
   Item Category: {order.get('ItemCateg', 'N/A')}

🏢 Organization
   Sales Organization: {order.get('Vkorg', 'N/A')}
   Distribution Channel: {order.get('Vtweg', 'N/A')}
   Sales Office: {order.get('Vkbur', 'N/A')}
   Division: {order.get('Spart', 'N/A')}

💰 Pricing
   Currency: {order.get('Waerk', 'N/A')}
   Condition Type: {order.get('Kscha', 'N/A')}
   Price Unit: {order.get('Kpein', 'N/A')}

📅 Dates
   Requested Delivery Date: {order.get('Edatu', 'N/A')}
   Customer Request Date: {order.get('Bstdk', 'N/A')}

{'=' * 50}
"""
        return response

    async def process_query(self, user_query: str) -> str:
        """Process user query and return response

        Args:
            user_query: User's natural language query

        Returns:
            Formatted response string
        """
        print(f"\n{'=' * 60}")
        print(f"💬 User Query: {user_query}")
        print(f"{'=' * 60}")

        # Step 1: Extract order ID using Gemini
        order_id = self.extract_order_id(user_query)

        if not order_id:
            return """
❌ Order number not found in your query.

Please ask in one of these formats:
- "Show me information for order 91000092"
- "What's the status of order 91000092?"
- "Order 91000092 details"
"""

        # Step 2: Retrieve order information from SAP
        order_data = await self.get_order_info(order_id)

        if not order_data:
            return f"❌ Order information not found for order number {order_id}."

        # Step 3: Format and return response
        return self.format_order_response(order_data, order_id)


async def main():
    """Main function to run the chatbot"""

    # Configuration
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        return

    # SAP Configuration (only business parameters - credentials from .env.server)
    sap_config = {
        "service": "Z_SALES_ORDER_GENAI_SRV",
        "entity_set": "zsd004Set",
    }

    # Initialize chatbot
    print("📝 SAP credentials loaded from .env.server file")
    chatbot = OrderInquiryChatbot(gemini_api_key, sap_config)

    print("\n" + "=" * 60)
    print("🤖 AI Order Inquiry Chatbot Started")
    print("=" * 60)

    # Interactive mode
    print("\n💡 Enter 'quit' or 'exit' to stop\n")

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye!")
                break

            if not user_input:
                continue

            # Process query
            response = await chatbot.process_query(user_input)
            print(f"\n🤖 Chatbot:\n{response}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

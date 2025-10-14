# 🤖 AI Order Inquiry Chatbot

An intelligent chatbot that uses Google Gemini AI to understand natural language queries and retrieve SAP order information through the MCP (Model Context Protocol) server.

## 🌟 Features

- **Natural Language Understanding**: Powered by Gemini 2.0 Flash to extract order IDs from conversational queries
- **Multi-Language Support**: Handles both Korean (한국어) and English queries
- **SAP Integration**: Retrieves real-time order data from SAP Gateway via MCP
- **User-Friendly Output**: Formats complex SAP data into readable, structured responses
- **Interactive Mode**: Real-time conversational interface for order inquiries

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                 User Input                             │
│  "주문 번호 91000092 정보 알려줘"                        │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│         Gemini AI (Order ID Extractor)                 │
│  Input: Natural language query                         │
│  Output: "91000092"                                    │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│              SAP MCP Client                            │
│  Tool: sap_get_entity                                  │
│  Service: Z_SALES_ORDER_GENAI_SRV                      │
│  Entity: zsd004Set('91000092')                         │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│            Response Formatter                          │
│  Formats SAP JSON → User-friendly text                │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│              Display to User                           │
│  📦 주문 정보 (Order Information)                       │
│  🔢 주문 번호: 91000092                                │
│  📝 고객 주문 번호: 2410_110440_01                     │
│  ...                                                   │
└────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

1. **Python 3.11+**
2. **Google Gemini API Key**
   - Get from: https://aistudio.google.com/app/apikey
3. **SAP Gateway Access**
   - SAP server hostname and credentials
   - OData service access
4. **MCP Server Running**
   - SAP MCP server must be running

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Google Gemini SDK
pip install google-genai

# Ensure MCP and SAP dependencies are installed
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Set Gemini API Key
export GEMINI_API_KEY="your-gemini-api-key"

# Verify it's set
echo $GEMINI_API_KEY
```

### 3. Configure SAP Settings

Edit `order_inquiry_chatbot.py` to configure your SAP connection:

```python
sap_config = {
    "host": "your-sap-server.com",
    "username": "your-username",
    "password": "your-password",
    "client": "100",
    "service": "Z_SALES_ORDER_GENAI_SRV",
    "entity_set": "zsd004Set",
}
```

### 4. Run the Chatbot

```bash
python order_inquiry_chatbot.py
```

## 💬 Usage Examples

### Example 1: Korean Query
```
👤 You: 주문 번호 91000092에 대한 정보를 알려줘

🤖 Chatbot:
📦 주문 정보 (Order Information)
==================================================

🔢 주문 번호 (Order ID): 91000092
📝 고객 주문 번호 (Customer PO): 2410_110440_01
📋 주문 유형 (Order Type): ZEX

👤 고객 정보 (Customer Information)
   고객 번호 (Customer No.): 110440

📦 품목 정보 (Item Information)
   자재 번호 (Material No.): B-ASCL01-086A
   주문 수량 (Quantity): 10
   품목 범주 (Item Category): ZEX
...
```

### Example 2: English Query
```
👤 You: Can you check order 91000092?

🤖 Chatbot:
[Same formatted order information]
```

### Example 3: Casual Korean Query
```
👤 You: 91000092 주문 상태는?

🤖 Chatbot:
[Same formatted order information]
```

### Example 4: No Order ID
```
👤 You: 주문 정보 알려줘

🤖 Chatbot:
❌ 주문 번호를 찾을 수 없습니다.

다음과 같은 형식으로 질문해주세요:
- "주문 번호 91000092에 대한 정보 알려줘"
- "91000092 주문 상태는?"
- "Order 91000092 details"
```

## 🔧 How It Works

### 1. Order ID Extraction (Gemini AI)

The chatbot uses Gemini with a specialized system instruction:

```python
system_instruction = """You are an order ID extraction assistant.
Extract the order ID (주문 번호) from the user's query.

Rules:
1. Order IDs are typically 8-digit numbers (e.g., 91000092)
2. Return ONLY the order ID number, nothing else
3. If no order ID is found, return "NONE"
"""
```

**Supported Query Formats**:
- "주문 번호 91000092 정보 알려줘"
- "Can you check order 91000092?"
- "91000092 주문 상태는?"
- "Order number 91000092 details"
- "91000092" (just the number)

### 2. SAP Data Retrieval (MCP Client)

The chatbot connects to the SAP MCP server using stdio transport:

```python
# Initialize MCP client
server_params = StdioServerParameters(
    command="python",
    args=["-m", "sap_mcp.stdio_server"]
)

# Authenticate
await session.call_tool("sap_authenticate", {...})

# Get order data
await session.call_tool("sap_get_entity", {
    "service": "Z_SALES_ORDER_GENAI_SRV",
    "entity_set": "zsd004Set",
    "entity_key": "91000092"
})
```

### 3. Response Formatting

The chatbot formats SAP JSON data into structured, bilingual (Korean/English) output:

```python
def format_order_response(order_data: Dict[str, Any]) -> str:
    """Format order data with emojis and bilingual labels"""
    return """
📦 주문 정보 (Order Information)
🔢 주문 번호 (Order ID): {OrderId}
📝 고객 주문 번호 (Customer PO): {Bstnk}
...
"""
```

## 🎯 Key Components

### `OrderInquiryChatbot` Class

```python
class OrderInquiryChatbot:
    def __init__(self, gemini_api_key: str, sap_config: Dict[str, str]):
        """Initialize with Gemini API and SAP configuration"""

    def extract_order_id(self, user_query: str) -> Optional[str]:
        """Use Gemini to extract order ID from natural language"""

    async def get_order_info(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve order data from SAP via MCP"""

    def format_order_response(self, order_data: Dict[str, Any]) -> str:
        """Format SAP data into user-friendly response"""

    async def process_query(self, user_query: str) -> str:
        """End-to-end query processing pipeline"""
```

## 🔒 Security Considerations

1. **API Key Management**: Store `GEMINI_API_KEY` in environment variables, not in code
2. **SAP Credentials**: Consider using secret management services for production
3. **Input Validation**: Order IDs are validated as numeric before SAP queries
4. **Error Handling**: Comprehensive error handling prevents sensitive data exposure

## 🧪 Testing

### Test with Sample Queries

```python
test_queries = [
    "주문 번호 91000092에 대한 정보를 알려줘",
    "Can you check order 91000092?",
    "91000092 주문 상태 확인해줘",
    "Order number 91000092 details please",
]

for query in test_queries:
    response = await chatbot.process_query(query)
    print(response)
```

### Expected Order Data Fields

The chatbot displays the following SAP order information:

| Field | Korean | English |
|-------|--------|---------|
| OrderId | 주문 번호 | Order ID |
| Bstnk | 고객 주문 번호 | Customer PO |
| Auart | 주문 유형 | Order Type |
| Kunnr | 고객 번호 | Customer No. |
| Matnr | 자재 번호 | Material No. |
| Wmeng | 주문 수량 | Quantity |
| Waerk | 통화 | Currency |
| Vkorg | 판매 조직 | Sales Org |
| Vtweg | 유통 채널 | Distribution Channel |
| Edatu | 요청 납기 | Requested Date |

## 🚧 Troubleshooting

### Issue: "GEMINI_API_KEY environment variable not set"
**Solution**:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Issue: "SAP authentication failed"
**Solution**:
- Verify SAP credentials in `sap_config`
- Ensure SAP MCP server is running
- Check network connectivity to SAP server

### Issue: "No order ID found in query"
**Solution**:
- Include the order number in your query
- Use 8-digit order IDs (e.g., 91000092)
- Try explicit formats: "주문 번호 91000092" or "order 91000092"

### Issue: "Order data not found"
**Solution**:
- Verify the order ID exists in SAP
- Check `service` and `entity_set` configuration
- Ensure user has access to the OData service

## 🔮 Future Enhancements

- [ ] **Multi-Order Support**: Handle queries with multiple order IDs
- [ ] **Order Status Tracking**: Real-time delivery status updates
- [ ] **Voice Input**: Speech-to-text integration
- [ ] **Chat History**: Maintain conversation context
- [ ] **Export Options**: Export order data to PDF/Excel
- [ ] **Notification System**: Alert users on order status changes
- [ ] **Advanced NLU**: Handle more complex queries (date ranges, filters)
- [ ] **Web UI**: React-based web interface

## 📚 Related Documentation

- [SAP MCP Server README](README.md)
- [MCP Protocol Specification](https://github.com/anthropics/mcp)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [SAP OData Documentation](https://help.sap.com/docs/SAP_NETWEAVER_750/68bf513362174d54b58cddec28794093/7b2b9e2ecc924b4ba50d53443f51b043.html)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Additional language support

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for natural language understanding
- Model Context Protocol (MCP) for standardized AI integration
- SAP Gateway for enterprise data access

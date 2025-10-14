# 🏗️ AI Order Inquiry Chatbot - Architecture Documentation

## System Overview

The AI Order Inquiry Chatbot is a multi-component system that combines natural language processing (Gemini AI), enterprise data access (SAP Gateway via MCP), and intelligent response formatting to provide conversational order information retrieval.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  Input Examples:                                                │
│  - "주문 번호 91000092 정보 알려줘"                              │
│  - "Can you check order 91000092?"                              │
│  - "91000092 주문 상태는?"                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Natural Language Query
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              GEMINI AI - ORDER ID EXTRACTOR                     │
│                                                                 │
│  Model: gemini-2.0-flash-exp                                    │
│  Temperature: 0 (deterministic)                                 │
│                                                                 │
│  System Instruction:                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ "Extract the order ID from the user's query"            │  │
│  │ Rules:                                                   │  │
│  │ 1. Order IDs are 8-digit numbers                        │  │
│  │ 2. Return ONLY the number                               │  │
│  │ 3. Return "NONE" if not found                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Input: "주문 번호 91000092 정보 알려줘"                         │
│  Output: "91000092"                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Extracted Order ID
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MCP CLIENT - SAP GATEWAY                      │
│                                                                 │
│  Transport: stdio (stdin/stdout)                                │
│  Server Command: python -m sap_mcp.stdio_server                 │
│                                                                 │
│  Step 1: Authentication                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Tool: sap_authenticate                                   │  │
│  │ Input: {host, username, password, client}                │  │
│  │ Output: {success, message, host, client}                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Step 2: Entity Retrieval                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Tool: sap_get_entity                                     │  │
│  │ Input: {                                                 │  │
│  │   service: "Z_SALES_ORDER_GENAI_SRV"                     │  │
│  │   entity_set: "zsd004Set"                                │  │
│  │   entity_key: "91000092"                                 │  │
│  │ }                                                        │  │
│  │ Output: {success, service, entity_set, data}             │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ SAP Order Data (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SAP GATEWAY (OData v2)                         │
│                                                                 │
│  Endpoint:                                                      │
│  https://34.64.166.83:44300/sap/opu/odata/SAP/                 │
│  Z_SALES_ORDER_GENAI_SRV/zsd004Set('91000092')                 │
│                                                                 │
│  Authentication:                                                │
│  - CSRF Token: X-CSRF-Token header                             │
│  - Session Cookie: SAP_SESSIONID_S4S_100                       │
│  - Basic Auth: Base64(username:password)                       │
│                                                                 │
│  Request Headers:                                               │
│  - Accept: application/json                                    │
│  - X-CSRF-Token: <token>                                       │
│  - Authorization: Basic <credentials>                          │
│  - Cookie: SAP_SESSIONID_S4S_100=<session>                     │
│                                                                 │
│  Response Format:                                               │
│  {                                                              │
│    "d": {                                                       │
│      "OrderId": "91000092",                                     │
│      "Bstnk": "2410_110440_01",                                 │
│      "Auart": "ZEX",                                            │
│      "Vkorg": "1000",                                           │
│      ...                                                        │
│    }                                                            │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Raw SAP JSON
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE FORMATTER                           │
│                                                                 │
│  Function: format_order_response()                              │
│                                                                 │
│  Transformations:                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Extract 'd' object from response                      │  │
│  │ 2. Map SAP fields to user-friendly labels                │  │
│  │ 3. Add emoji indicators                                  │  │
│  │ 4. Format bilingual (Korean/English)                     │  │
│  │ 5. Structure by information categories                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Categories:                                                    │
│  - 주문 정보 (Order Information)                                │
│  - 고객 정보 (Customer Information)                             │
│  - 품목 정보 (Item Information)                                 │
│  - 조직 정보 (Organization)                                     │
│  - 가격 정보 (Pricing)                                          │
│  - 날짜 정보 (Dates)                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Formatted Response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       USER DISPLAY                              │
│                                                                 │
│  📦 주문 정보 (Order Information)                                │
│  ══════════════════════════════════════════════                 │
│                                                                 │
│  🔢 주문 번호 (Order ID): 91000092                              │
│  📝 고객 주문 번호 (Customer PO): 2410_110440_01                │
│  📋 주문 유형 (Order Type): ZEX                                 │
│                                                                 │
│  👤 고객 정보 (Customer Information)                            │
│     고객 번호 (Customer No.): 110440                            │
│                                                                 │
│  📦 품목 정보 (Item Information)                                │
│     자재 번호 (Material No.): B-ASCL01-086A                     │
│     주문 수량 (Quantity): 10                                    │
│     품목 범주 (Item Category): ZEX                              │
│                                                                 │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

**Purpose**: Accept natural language input from users

**Input Formats Supported**:
- Korean formal: "주문 번호 91000092에 대한 정보를 알려줘"
- Korean casual: "91000092 주문 상태는?"
- English formal: "Can you check order 91000092?"
- English brief: "Order 91000092 details"
- Number only: "91000092"

**Technologies**:
- Python `input()` for interactive mode
- Could be extended to: Web UI, Slack bot, SMS, Voice

### 2. Gemini AI - Natural Language Understanding

**Purpose**: Extract structured data (order IDs) from unstructured text

**Model**: `gemini-2.0-flash-exp`
- Fast response time (~1-2 seconds)
- Cost-effective for production
- High accuracy for extraction tasks

**Configuration**:
```python
config = types.GenerateContentConfig(
    temperature=0,  # Deterministic output
    system_instruction=[...],
)
```

**System Instruction Design**:
- Clear extraction rules
- Return format specification
- Fallback handling ("NONE")
- No additional explanations

**Error Handling**:
- Invalid responses → None
- Non-numeric output → None
- Empty responses → None
- API errors → Logged and None

### 3. MCP Client - Protocol Bridge

**Purpose**: Bridge between Python and SAP MCP server using stdio

**Architecture**:
```python
StdioServerParameters
    ↓
stdio_client (read, write streams)
    ↓
ClientSession (MCP protocol handling)
    ↓
Tool calls (sap_authenticate, sap_get_entity)
```

**Communication Flow**:
1. **Initialization**: Establish stdio connection
2. **Session Setup**: Create MCP client session
3. **Authentication**: Call `sap_authenticate` tool
4. **Data Retrieval**: Call `sap_get_entity` tool
5. **Response Parsing**: Extract data from MCP wrapper

**Response Format** (MCP):
```python
CallToolResult(
    content=[
        TextContent(
            type='text',
            text='[{\'type\': \'text\', \'text\': "{...}"}]'
        )
    ]
)
```

### 4. SAP Gateway - Enterprise Data Source

**Purpose**: Provide OData access to SAP business data

**Protocol**: OData v2
**Transport**: HTTPS
**Authentication**: Basic Auth + CSRF Token

**Request Lifecycle**:
```
1. CSRF Token Fetch
   GET /sap/opu/odata/SAP/Z_SALES_ORDER_GENAI_SRV/zsd004Set
   Headers: X-CSRF-Token: Fetch

2. Token Received
   Response Headers:
   - X-CSRF-Token: <token>
   - Set-Cookie: SAP_SESSIONID_S4S_100=<session>

3. Entity Retrieval
   GET /sap/opu/odata/SAP/Z_SALES_ORDER_GENAI_SRV/zsd004Set('91000092')
   Headers:
   - Accept: application/json
   - X-CSRF-Token: <token>
   - Cookie: SAP_SESSIONID_S4S_100=<session>
   - Authorization: Basic <credentials>

4. JSON Response
   {
     "d": {
       "OrderId": "91000092",
       ...
     }
   }
```

**SSL Handling**:
- Self-signed certificates supported
- SSL context configured in client
- `verify_ssl=False` for development

### 5. Response Formatter - Data Presentation

**Purpose**: Transform SAP JSON into user-friendly text

**Transformation Pipeline**:
```
Raw SAP JSON
    ↓
Extract 'd' object
    ↓
Map field names to labels
    ↓
Add emoji indicators
    ↓
Group by categories
    ↓
Format bilingual labels
    ↓
Structured text output
```

**Field Mapping Example**:
```python
{
    "OrderId": "🔢 주문 번호 (Order ID)",
    "Bstnk": "📝 고객 주문 번호 (Customer PO)",
    "Auart": "📋 주문 유형 (Order Type)",
    ...
}
```

**Categories**:
1. **Order Information**: ID, type, PO number
2. **Customer Information**: Customer number
3. **Item Information**: Material, quantity, category
4. **Organization**: Sales org, channel, office
5. **Pricing**: Currency, conditions
6. **Dates**: Requested date, customer date

## Data Flow Sequence

```
[User]
  ↓ "주문 번호 91000092 정보 알려줘"
[Chatbot.process_query()]
  ↓
[Chatbot.extract_order_id()]
  ↓ Call Gemini API
[Gemini AI]
  ↓ "91000092"
[Chatbot.get_order_info()]
  ↓ Initialize MCP Client
[MCP Client Session]
  ↓ call_tool("sap_authenticate")
[SAP MCP Server] → [SAP Gateway]
  ↓ CSRF Token + Session Cookie
[MCP Client Session]
  ↓ call_tool("sap_get_entity")
[SAP MCP Server] → [SAP Gateway]
  ↓ OData GET with entity key
[SAP Gateway]
  ↓ JSON Response
[MCP Client Session]
  ↓ Parse MCP response
[Chatbot.format_order_response()]
  ↓ Format to user-friendly text
[User]
  ↓ Display formatted response
```

## Error Handling Strategy

### 1. Gemini Extraction Errors
- **API Failure**: Return None, display error message
- **Invalid Format**: Return None, ask for valid order ID
- **No Match**: Return None, show example queries

### 2. SAP Authentication Errors
- **Invalid Credentials**: Log error, display auth failed message
- **Network Error**: Retry with exponential backoff (handled by MCP client)
- **SSL Error**: Verify SSL configuration

### 3. SAP Data Retrieval Errors
- **Order Not Found**: Display "Order not found" message
- **Permission Denied**: Display access error
- **Timeout**: Display timeout message, suggest retry

### 4. Response Parsing Errors
- **Invalid JSON**: Log error, display raw response
- **Missing Fields**: Display "N/A" for missing data
- **Malformed Data**: Log error, display partial data

## Performance Considerations

### Response Times
- **Gemini Extraction**: ~1-2 seconds
- **SAP Authentication**: ~2-3 seconds (cached after first call)
- **SAP Data Retrieval**: ~1-2 seconds
- **Response Formatting**: <0.1 seconds
- **Total**: ~4-7 seconds per query

### Optimization Opportunities
1. **Token Caching**: Reuse SAP authentication tokens (implemented)
2. **Session Pooling**: Maintain open MCP connections
3. **Response Caching**: Cache recent order lookups
4. **Batch Processing**: Handle multiple order IDs in one query
5. **Async Processing**: Parallel Gemini and SAP calls

## Security Architecture

### API Key Management
- Gemini API key stored in environment variable
- Never committed to source control
- Rotated periodically

### SAP Credentials
- Passed through MCP client, not stored
- Use environment variables or secret managers
- Consider OAuth for production

### Data Protection
- No PII logged to console (except order IDs)
- Sensitive fields masked in logs
- HTTPS for all SAP communication

### Access Control
- User authentication (future enhancement)
- Role-based order access
- Audit logging for compliance

## Scalability Considerations

### Current Limitations
- Single-threaded processing
- One query at a time
- stdio transport (process per request)

### Scalability Options
1. **Web Server**: FastAPI + WebSocket transport
2. **Message Queue**: RabbitMQ for async processing
3. **Load Balancing**: Multiple MCP server instances
4. **Caching Layer**: Redis for order data
5. **Database**: PostgreSQL for chat history

## Extension Points

### 1. Multi-Language Support
Add more languages to Gemini extraction:
- Japanese: "注文番号 91000092"
- Chinese: "订单号 91000092"
- Spanish: "pedido 91000092"

### 2. Additional SAP Operations
- Order creation
- Order updates
- Delivery tracking
- Invoice retrieval

### 3. Advanced NLU
- Date range queries: "last week's orders"
- Customer queries: "orders for customer 110440"
- Status filters: "pending orders"

### 4. Integration Points
- Slack bot integration
- Microsoft Teams bot
- Web dashboard
- Mobile app
- Voice assistants (Alexa, Google Assistant)

## Monitoring & Observability

### Metrics to Track
- Query response times
- Gemini extraction accuracy
- SAP authentication success rate
- Order retrieval success rate
- Error rates by type

### Logging Strategy
- Structured JSON logging
- Correlation IDs for request tracing
- Error stack traces
- Performance metrics

### Alerting
- High error rates
- Slow response times
- Authentication failures
- SAP connectivity issues

## Deployment Architecture

### Development
```
Developer Machine
  ↓
Local Python Process
  ↓ stdio
Local MCP Server
  ↓ HTTPS
SAP Gateway (Test)
```

### Production (Proposed)
```
Users
  ↓ HTTPS
Load Balancer
  ↓
FastAPI Servers (multiple)
  ↓ HTTP/WebSocket
MCP Server Pool
  ↓ HTTPS
SAP Gateway (Production)
  ↓
Redis Cache
  ↓
PostgreSQL (Chat History)
```

## Technology Stack

### Core Technologies
- **Python 3.11+**: Main programming language
- **Google Gemini API**: Natural language understanding
- **MCP (Model Context Protocol)**: Standardized AI integration
- **SAP Gateway**: Enterprise data access
- **OData v2**: REST-like data protocol

### Key Libraries
```python
google-genai      # Gemini AI client
mcp               # Model Context Protocol
aiohttp           # Async HTTP client
asyncio           # Async programming
```

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Type checking
- **flake8**: Linting

## Conclusion

The AI Order Inquiry Chatbot demonstrates a clean, modular architecture that combines:
- Modern NLU (Gemini)
- Standardized protocols (MCP)
- Enterprise integration (SAP)
- User-friendly presentation

This architecture is extensible, maintainable, and production-ready with appropriate enhancements for scalability and monitoring.

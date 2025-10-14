# AI Order Inquiry Chatbot

An intelligent chatbot that provides natural language interface for querying SAP order information. Powered by Google Gemini AI and connected to SAP Gateway through MCP server.

## Features

### 🤖 Natural Language Processing
- **Multilingual Support**: Understands both Korean and English queries
- **Flexible Query Format**: Accepts various natural language patterns
- **Smart Order ID Extraction**: Automatically extracts order IDs from conversation

### 💬 Interactive Interface
- **Real-time Conversation**: Interactive command-line interface
- **Conversation History**: Tracks recent queries and responses
- **Command Shortcuts**: Built-in commands for better usability
- **Graceful Error Handling**: User-friendly error messages

### 🔐 Secure Configuration
- **Environment-based Credentials**: SAP credentials loaded from `.env.server`
- **No Hardcoded Secrets**: All sensitive data in environment variables
- **MCP Integration**: Secure connection through MCP stdio server

## Files Overview

```
sap-mcp/
├── interactive_chatbot.py      # Main interactive chatbot (NEW)
├── order_inquiry_chatbot.py    # Core chatbot logic
├── test_chatbot.py             # Automated testing script
├── .env.server                 # SAP credentials (git-ignored)
└── .env.client                 # Client config (optional, git-ignored)
```

## Quick Start

### Prerequisites

1. **Python 3.11+** installed
2. **SAP Gateway Access** with valid credentials
3. **Google Gemini API Key** ([Get one here](https://ai.google.dev/))

### Setup

```bash
# 1. Ensure SAP credentials are in .env.server
cat .env.server  # Should contain SAP_HOST, SAP_USERNAME, SAP_PASSWORD

# 2. Set Gemini API key
export GEMINI_API_KEY='your-gemini-api-key-here'

# 3. Install dependencies (if not already installed)
pip install -r requirements.txt
```

### Run Interactive Chatbot

```bash
python interactive_chatbot.py
```

### Run Automated Tests

```bash
python test_chatbot.py
```

## Usage Examples

### Interactive Mode

```
╔════════════════════════════════════════════════════════════════════╗
║              🤖 AI Order Inquiry Chatbot Started 🚀                ║
╚════════════════════════════════════════════════════════════════════╝

👤 You: 주문 번호 91000092 정보 알려줘

⏳ Processing your request...

🤖 Response:
📦 주문 정보 (Order Information)
==================================================

🔢 주문 번호 (Order ID): 91000092
📝 고객 주문 번호 (Customer PO): 2410_110440_01
📋 주문 유형 (Order Type): ZEX
...

👤 You: help

📖 AVAILABLE COMMANDS:
  help, ?          Show this help message
  history          Show recent conversation history
  clear            Clear conversation history
  quit, exit, q    Exit the chatbot
...
```

### Query Formats

The chatbot understands various natural language formats:

**Korean**:
```
주문 번호 91000092 정보 알려줘
91000092 주문 상태는?
91000093 확인해줘
```

**English**:
```
Can you check order 91000092?
Order 91000092 details please
What's the status of 91000093?
```

**Just the Number**:
```
91000092
```

## Available Commands

| Command | Description |
|---------|-------------|
| `help` or `?` | Show help message and examples |
| `history` | Display recent conversation history |
| `clear` | Clear conversation history |
| `quit`, `exit`, or `q` | Exit the chatbot |

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Interactive Chatbot                       │
│  - User input handling                                       │
│  - Command processing                                        │
│  - Conversation history                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Order Inquiry Chatbot                       │
│  - Natural language processing (Gemini AI)                   │
│  - Order ID extraction                                       │
│  - Response formatting                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (stdio)                        │
│  - Connect to SAP MCP server                                 │
│  - Call tools: sap_authenticate, sap_get_entity             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     SAP MCP Server                           │
│  - Load credentials from .env.server                         │
│  - Authenticate with SAP Gateway                             │
│  - Execute OData queries                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      SAP Gateway                             │
│  - OData v2 API                                              │
│  - Sales order data (Z_SALES_ORDER_GENAI_SRV)               │
└─────────────────────────────────────────────────────────────┘
```

### Workflow

1. **User Input**: User types a natural language query
2. **Command Processing**: Check if it's a command (help, history, etc.)
3. **NL Processing**: Extract order ID using Gemini AI
4. **MCP Call**: Connect to SAP via MCP stdio server
5. **Authentication**: Server authenticates with SAP (credentials from `.env.server`)
6. **Query Execution**: Retrieve order data via OData
7. **Response Formatting**: Format data in user-friendly format
8. **Display**: Show formatted response to user
9. **History**: Save conversation for future reference

## Configuration

### Environment Variables

**Required** (in `.env.server`):
```bash
SAP_HOST=your-sap-server.com
SAP_USERNAME=your_username
SAP_PASSWORD=your_password
```

**Optional** (in `.env.server`):
```bash
SAP_PORT=44300
SAP_CLIENT=100
SAP_VERIFY_SSL=false
```

**Runtime** (shell environment):
```bash
export GEMINI_API_KEY='your-gemini-api-key'
```

### SAP Service Configuration

Default configuration in the code:
```python
sap_config = {
    "service": "Z_SALES_ORDER_GENAI_SRV",
    "entity_set": "zsd004Set",
}
```

To use a different service, modify the configuration in:
- `interactive_chatbot.py` (main function)
- `test_chatbot.py` (test function)

## Troubleshooting

### Common Issues

**1. GEMINI_API_KEY not set**
```
❌ Error: GEMINI_API_KEY environment variable not set

Solution:
export GEMINI_API_KEY='your-api-key-here'
```

**2. SAP credentials not found**
```
Authentication failed: Field required [type=missing, input_value={}, input_type=dict]

Solution:
# Check .env.server file exists and has correct values
cat .env.server
```

**3. Order ID not found**
```
❌ No order ID found in query

Solution:
# Make sure your query includes an 8-digit order number
# Examples: "주문 91000092 정보", "Order 91000092", "91000092"
```

**4. MCP server connection failed**
```
Error retrieving order: [connection error]

Solution:
# Ensure the MCP server module is installed
pip install -r requirements.txt

# Check if .env.server has correct SAP credentials
cat .env.server
```

### Debug Mode

To enable detailed logging, modify the chatbot code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Testing

**Run automated tests**:
```bash
python test_chatbot.py
```

**Test specific query**:
```python
python interactive_chatbot.py
# Then type your test query
```

### Code Quality

**Linting**:
```bash
python -m flake8 interactive_chatbot.py --max-line-length=100
```

**Type Checking** (if using mypy):
```bash
mypy interactive_chatbot.py
```

## Security Best Practices

1. **Never commit credentials**
   - `.env.server` and `.env.client` are in `.gitignore`
   - Use environment variables for API keys

2. **Secure API access**
   - Keep Gemini API key private
   - Rotate SAP credentials regularly

3. **Network security**
   - Use SSL/TLS for SAP connections in production
   - Set `SAP_VERIFY_SSL=true` with valid certificates

4. **Code review**
   - Review all code before deployment
   - Use linting and type checking

## Performance Considerations

- **Conversation History**: Limited to 50 entries (configurable via `max_history`)
- **Response Caching**: Not implemented (future enhancement)
- **Connection Pooling**: MCP server handles connection management
- **Timeout**: Default 30 seconds for SAP queries (configurable in `.env.server`)

## Future Enhancements

- [ ] **Response Caching**: Cache frequent queries to reduce SAP load
- [ ] **Multi-language UI**: Support more languages
- [ ] **Voice Interface**: Add voice input/output
- [ ] **Web Interface**: Create web-based chat UI
- [ ] **Analytics**: Track query patterns and performance
- [ ] **Batch Queries**: Support multiple order lookups
- [ ] **Export**: Save conversation history to file

## License

This project is part of the SAP MCP Server. See main project LICENSE for details.

## Support

For issues and questions:
- Check this README first
- Review main project documentation
- Check SAP Gateway connectivity
- Verify Gemini API key and quota

# SAP MCP Examples

Working examples demonstrating how to use the SAP MCP Server with various client applications.

## 📋 Table of Contents

- [Overview](#overview)
- [Available Examples](#available-examples)
- [Prerequisites](#prerequisites)
- [Running Examples](#running-examples)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This directory contains practical examples showing different ways to interact with the SAP MCP Server:

- **Basic MCP Client**: Direct MCP protocol usage via stdio transport
- **AI Chatbot**: Natural language order inquiry with Gemini AI
- **GenAI Integration**: Google Generative AI integration patterns

All examples use the **stdio transport** for communication with the MCP server.

## 📁 Available Examples

### 1. Basic MCP Client

**Location**: `packages/client/examples/stdio_client_get.py`

Simple example demonstrating direct MCP protocol communication.

**Features**:
- SAP authentication
- Entity retrieval by key
- Response parsing and formatting
- Error handling

**Use Case**: Learning MCP protocol basics, simple SAP queries

### 2. AI Order Inquiry Chatbot

**Location**: `packages/client/examples/order_inquiry_chatbot.py`

Interactive chatbot that understands natural language queries about SAP orders.

**Features**:
- Natural language processing with Gemini AI
- Order ID extraction from user queries
- Interactive command-line interface
- Formatted order information display

**Example Queries**:
- "Show me information for order 91000043"
- "What's the status of order 91000043?"
- "Order 91000043 details please"

**Use Case**: Building AI-powered SAP integration chatbots

### 3. GenAI Integration

**Location**: `packages/client/examples/genai-example.py`

Example showing integration with Google Generative AI.

**Features**:
- Gemini API integration
- MCP tool orchestration
- Async/await patterns

**Use Case**: AI-powered SAP data analysis and automation

## 🔧 Prerequisites

### 1. Server Package Installation

```bash
# Navigate to server package
cd packages/server

# Install in development mode
pip install -e .
```

### 2. SAP Credentials Configuration

⚠️ **Important**: Configure `.env.server` with your actual SAP credentials.

**Location**: `packages/server/.env.server`

```bash
# SAP Gateway Connection
SAP_HOST=your-sap-server.com
SAP_PORT=443
SAP_USERNAME=your-username
SAP_PASSWORD=your-password
SAP_CLIENT=100

# Connection Settings
SAP_VERIFY_SSL=true
SAP_TIMEOUT=30
```

**Verify Configuration** (optional):

```bash
cd packages/server
python -c "from sap_mcp_server.config.settings import get_sap_config; print(get_sap_config())"
```

### 3. Client Package Installation (Optional)

```bash
# Navigate to client package
cd packages/client

# Install in development mode
pip install -e .

# For AI examples, install with examples dependencies
pip install -e ".[examples]"
```

### 4. Gemini API Key (For AI Examples)

```bash
# Set environment variable
export GEMINI_API_KEY="your-gemini-api-key"
```

Get your API key from: https://ai.google.dev/

## 🚀 Running Examples

### Basic MCP Client

```bash
cd packages/client
python examples/stdio_client_get.py
```

**Expected Output**:

```
🚀 SAP MCP Client - Stdio Mode
============================================================

📡 Initializing MCP session...
✅ Session initialized

=== SAP Authentication ===
✅ Authentication successful

=== Get Entity (OrderID: 91000043) ===
✅ Entity retrieved successfully
{
  "OrderID": "91000043",
  "Bstnk": "PO-2024-001",
  ...
}

✅ Test completed
```

### AI Order Inquiry Chatbot

```bash
# Set Gemini API key
export GEMINI_API_KEY="your-api-key"

# Run chatbot
cd packages/client
python examples/order_inquiry_chatbot.py
```

**Interactive Session**:

```
🤖 AI Order Inquiry Chatbot Started
============================================================

💡 Enter 'quit' or 'exit' to stop

👤 You: Show me information for order 91000043

🤔 Analyzing query: 'Show me information for order 91000043'
✅ Extracted Order ID: 91000043
📡 Retrieving order information from SAP...
✅ Order data retrieved successfully

🤖 Chatbot:

📦 Order Information
==================================================

🔢 Order ID: 91000043
📝 Customer PO Number: PO-2024-001
📋 Order Type: TA

👤 Customer Information
   Customer Number: CUST001

...
```

### GenAI Integration

```bash
cd packages/client
python examples/genai-example.py
```

## ⚙️ Claude Desktop Integration

To use SAP MCP Server with Claude Desktop:

**1. Edit Configuration File**:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

**2. Add Server Configuration**:

```json
{
  "mcpServers": {
    "sap-mcp": {
      "command": "python",
      "args": ["-m", "sap_mcp_server.transports.stdio"],
      "env": {
        "SAP_HOST": "your-sap-server.com",
        "SAP_PORT": "443",
        "SAP_USERNAME": "your-username",
        "SAP_PASSWORD": "your-password",
        "SAP_CLIENT": "100",
        "SAP_VERIFY_SSL": "true"
      }
    }
  }
}
```

**3. Restart Claude Desktop**

## 🔧 Troubleshooting

### 1. ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'sap_mcp_server'`

**Solution**:

```bash
cd packages/server
pip install -e .
```

### 2. Authentication Failed

**Error**: `Authentication failed: 3 validation errors for SAPConnectionConfig`

**Solution**:

1. Verify `.env.server` file location:
   ```bash
   ls -la packages/server/.env.server
   ```

2. Check credentials are set:
   ```bash
   cat packages/server/.env.server | grep SAP_
   ```

3. Ensure actual values (not placeholders):
   - ❌ `SAP_HOST=your-sap-server.com` (placeholder)
   - ✅ `SAP_HOST=actual-server.company.com` (actual value)

4. Correct variable names:
   - ✅ `SAP_HOST`, `SAP_PORT`, `SAP_USERNAME`, `SAP_PASSWORD`, `SAP_CLIENT`

### 3. Connection Closed

**Error**: Server process fails to start

**Solution**:

1. Verify server package installation:
   ```bash
   pip list | grep sap-mcp-server
   ```

2. Test server directly:
   ```bash
   cd packages/server
   python -m sap_mcp_server.transports.stdio
   ```

3. Check logs for error messages

### 4. SAP Connection Error

**Error**: `SAP connection error: Connection refused`

**Solution**:

1. Verify SAP server URL and port
2. Check network connectivity
3. Verify firewall settings
4. For SSL issues, use `SAP_VERIFY_SSL=false` (development only)

### 5. Gemini API Error

**Error**: `GEMINI_API_KEY environment variable not set`

**Solution**:

```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

## 📚 Additional Resources

- **[Main README](../README.md)**: Project overview
- **[Server Documentation](../packages/server/README.md)**: Server package details
- **[Client Documentation](../packages/client/README.md)**: Client SDK guide
- **[Configuration Guide](../docs/guides/configuration.md)**: Setup instructions
- **[Deployment Guide](../docs/guides/deployment.md)**: Production deployment

## 💡 Tips

1. **Environment Variables**: Use `.env.server` for safe credential management
2. **Debugging**: Set log level for detailed logs
3. **Performance**: Use `$top` and `$skip` parameters for large datasets
4. **Security**: Use `SAP_VERIFY_SSL=true` in production

## 🔐 Security Notes

- **Never commit** `.env.server` to version control
- Use environment variables or secret management tools in production
- Enable SSL certificate verification in production
- Set restrictive file permissions: `chmod 600 .env.server`
- Monitor SAP audit logs for suspicious activity

## 🛠️ Creating Your Own Example

### Basic Template

```python
"""My SAP MCP Example"""
import asyncio
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    # Configure server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"]
    )

    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            # Authenticate with SAP
            auth_result = await session.call_tool("sap_authenticate", {})
            print("Authentication:", auth_result)

            # Your code here
            # ...

if __name__ == "__main__":
    asyncio.run(main())
```

### Steps to Create

1. Copy template to new file in `packages/client/examples/`
2. Add your custom logic
3. Test with `python examples/your_example.py`
4. Document in this README
5. Add integration tests if needed

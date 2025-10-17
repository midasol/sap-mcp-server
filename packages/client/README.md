# SAP MCP Client

High-level Python client library and examples for interacting with SAP MCP Server.

## 🎯 Overview

The SAP MCP Client package provides Python client SDK and example applications demonstrating how to interact with the SAP MCP Server for AI-powered SAP Gateway integration.

**Version**: 0.2.0
**Python**: 3.11+
**Status**: 📝 In Development

### Key Features

- 🤖 **AI Integration**: Gemini-powered order inquiry chatbot
- 📡 **MCP Client**: High-level client for SAP MCP Server
- 📝 **Examples**: Working code samples for common use cases
- 🚀 **Easy to Use**: Simple async/await API
- 🔧 **Modular**: Reusable components and transports

## 🚀 Quick Start

### Installation

```bash
# Navigate to client package
cd packages/client

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Install with examples dependencies
pip install -e ".[examples]"
```

### Basic Usage

```python
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    # Connect to SAP MCP Server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            # Authenticate with SAP
            auth_result = await session.call_tool("sap_authenticate", {})

            # Query orders
            query_result = await session.call_tool(
                "sap_query",
                {
                    "service": "Z_SALES_ORDER_GENAI_SRV",
                    "entity_set": "zsd004Set",
                    "filter": "OrderID eq '91000043'",
                    "top": 10
                }
            )
            print(query_result)
```

## 📦 Package Structure

```
src/sap_mcp_client/
├── __init__.py              # Package initialization
└── transports/              # Transport implementations
    └── __init__.py

examples/
├── stdio_client_get.py      # Basic MCP client example
├── order_inquiry_chatbot.py # AI chatbot with Gemini
└── genai-example.py         # GenAI integration example

tests/
├── unit/                    # Unit tests
└── integration/             # Integration tests
```

## 📚 Examples

### 1. Basic MCP Client

Simple example demonstrating direct MCP protocol usage.

```bash
# Run the basic client example
python examples/stdio_client_get.py
```

**Features**:
- Direct MCP protocol usage
- Session management
- Tool invocation
- Error handling

### 2. AI Order Inquiry Chatbot

AI-powered chatbot that understands natural language queries about SAP orders.

```bash
# Set up environment variables
export GEMINI_API_KEY="your-gemini-api-key"

# SAP credentials should be in ../../.env.server

# Run the chatbot
python examples/order_inquiry_chatbot.py
```

**Features**:
- Natural language processing with Gemini AI
- Order ID extraction from queries
- SAP order retrieval via MCP
- Formatted order information display

**Example Queries**:
- "Show me information for order 91000043"
- "What's the status of order 91000043?"
- "Order 91000043 details please"

### 3. GenAI Integration

Example showing integration with Google Generative AI.

```bash
python examples/genai-example.py
```

**Features**:
- Gemini API integration
- MCP tool orchestration
- Async/await patterns

## 🔧 Configuration

### Environment Variables

The client relies on the SAP MCP Server configuration. Ensure the server's `.env.server` file is properly configured:

```bash
# Server configuration (../../.env.server)
SAP_HOST=your-sap-host.com
SAP_PORT=443
SAP_USERNAME=your-username
SAP_PASSWORD=your-password
SAP_CLIENT=100
SAP_VERIFY_SSL=true
SAP_TIMEOUT=30
```

### Gemini API Key (for AI examples)

```bash
# For AI-powered examples
export GEMINI_API_KEY="your-gemini-api-key"
```

Get your API key from: https://ai.google.dev/

## 🧪 Testing

```bash
# Run all tests
python -m pytest -v

# Run unit tests only
python -m pytest -m unit

# Run integration tests
python -m pytest -m integration
```

## 🛠️ Development

### Adding a New Example

1. **Create Example File**: `examples/my_example.py`

```python
"""My Example Description"""
import asyncio
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Your code here

if __name__ == "__main__":
    asyncio.run(main())
```

2. **Add Documentation**: Update this README with example description

3. **Add Tests**: `tests/integration/test_my_example.py`

### Code Quality

```bash
# Format code
black src/ examples/

# Sort imports
isort src/ examples/

# Type check
mypy src/
```

## 📖 Available Tools

When connected to SAP MCP Server, these tools are available:

### sap_authenticate
Authenticate with SAP Gateway system.

### sap_query
Query SAP entities with OData filters.

**Parameters**:
- `service`: OData service name
- `entity_set`: Entity set name
- `filter`: OData filter expression
- `select`: Fields to select (optional)
- `top`: Maximum records (optional)
- `skip`: Skip records (optional)

### sap_get_entity
Retrieve a specific entity by key.

**Parameters**:
- `service`: OData service name
- `entity_set`: Entity set name
- `entity_key`: Entity key value

### sap_list_services
List all available SAP services from configuration.

## 🔒 Security

- **Credentials**: Server credentials stored in `.env.server` (parent directory)
- **API Keys**: Client API keys (e.g., Gemini) via environment variables
- **Transport**: Stdio transport uses local process communication
- **Validation**: All inputs validated by server before SAP calls

## 📚 Resources

- **[Main README](../../README.md)**: Project overview
- **[Server Documentation](../server/README.md)**: Server package details
- **[Configuration Guide](../../docs/guides/configuration.md)**: Setup guide
- **[Deployment Guide](../../docs/guides/deployment.md)**: Production deployment

## 📝 License

MIT License - see [LICENSE](../../LICENSE) file for details.

## 🆘 Support

- **Issues**: Create an issue in the main repository
- **Documentation**: See `../../docs/` directory
- **Server Package**: Check `../server/` directory

## 🗺️ Roadmap

### Current (v0.2.0)
- ✅ Basic MCP client examples
- ✅ AI-powered order inquiry chatbot
- ✅ Gemini integration examples

### Planned (v0.3.0)
- [ ] High-level client SDK (`SAPMCPClient` class)
- [ ] Session management utilities
- [ ] Response parsing helpers
- [ ] Retry and error handling utilities
- [ ] Type definitions and models
- [ ] Additional AI integration examples
- [ ] Client-side caching support

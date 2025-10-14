# SAP MCP Client

Python client library for connecting to SAP MCP Server via Model Context Protocol.

## Overview

SAP MCP Client is a lightweight Python library for integrating with SAP MCP Server. It supports both SSE (production) and stdio (development) transport modes.

## Features

- ✅ **SSE Transport**: Connect to remote SAP MCP servers via HTTP
- ✅ **Stdio Transport**: Local development and testing
- ✅ **Async Support**: Full async/await support
- ✅ **Type Safety**: Full type hints and Pydantic validation
- ✅ **Simple API**: Easy-to-use client interface

## Installation

```bash
pip install sap-mcp-client

# Or for development
pip install -e ".[dev]"
```

## Quick Start

### SSE Client (Production)

```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    # Connect to SSE server
    server_url = "http://sap-mcp-server:8000/sse"

    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            # Authenticate with SAP
            auth_result = await session.call_tool("sap_authenticate", {})
            print(f"Authenticated: {auth_result}")

            # Get entity
            entity = await session.call_tool(
                "sap_get_entity",
                {
                    "service": "Z_SALES_ORDER_SRV",
                    "entity_set": "SalesOrderSet",
                    "entity_key": "12345",
                },
            )
            print(f"Entity: {entity}")


asyncio.run(main())
```

### Stdio Client (Development)

```python
import asyncio
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client


async def main():
    # Start local server
    server_params = StdioServerParameters(
        command="sap-mcp-server-stdio"
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Use the same API as SSE client
            result = await session.call_tool("sap_authenticate", {})
            print(result)


asyncio.run(main())
```

## Configuration

### Environment Variables

Create `.env` file:

```bash
# SSE Server URL
SAP_MCP_SERVER_URL=http://localhost:8000/sse

# Optional: Client settings
MCP_CLIENT_TIMEOUT=30
MCP_CLIENT_RETRY_ATTEMPTS=3
```

### Python Configuration

```python
from dotenv import load_dotenv
import os

load_dotenv()

server_url = os.getenv("SAP_MCP_SERVER_URL", "http://localhost:8000/sse")
```

## Examples

See the `examples/` directory for complete examples:

- **`sse_client.py`**: Production SSE client example
- **`stdio_client.py`**: Development stdio client example
- **`advanced_client.py`**: Advanced usage patterns
- **`error_handling.py`**: Error handling best practices

### Running Examples

```bash
# SSE client example
cd examples
python sse_client.py

# Stdio client example
python stdio_client.py
```

## Available Tools

### Authentication

```python
# Authenticate with SAP
await session.call_tool("sap_authenticate", {})
```

### Get Entity

```python
# Get a specific entity by key
result = await session.call_tool(
    "sap_get_entity",
    {
        "service": "Z_SALES_ORDER_SRV",
        "entity_set": "SalesOrderSet",
        "entity_key": "12345",
    },
)
```

### Query Entities

```python
# Query entities with filters
result = await session.call_tool(
    "sap_query_entities",
    {
        "service": "Z_SALES_ORDER_SRV",
        "entity_set": "SalesOrderSet",
        "filter": "Status eq 'OPEN'",
        "top": 50,
        "skip": 0,
        "orderby": "CreatedDate desc",
    },
)
```

### Create Entity

```python
# Create a new entity
result = await session.call_tool(
    "sap_create_entity",
    {
        "service": "Z_SALES_ORDER_SRV",
        "entity_set": "SalesOrderSet",
        "data": {
            "CustomerID": "CUST001",
            "OrderDate": "2024-01-15",
            "TotalAmount": 1500.00,
        },
    },
)
```

### Update Entity

```python
# Update an existing entity
result = await session.call_tool(
    "sap_update_entity",
    {
        "service": "Z_SALES_ORDER_SRV",
        "entity_set": "SalesOrderSet",
        "entity_key": "12345",
        "data": {
            "Status": "COMPLETED",
            "CompletedDate": "2024-01-20",
        },
    },
)
```

## Error Handling

```python
from mcp.types import McpError

async def safe_call():
    try:
        result = await session.call_tool("sap_get_entity", {...})
        return result
    except McpError as e:
        print(f"MCP Error: {e.message}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Best Practices

### Connection Management

```python
# Use context managers for automatic cleanup
async with sse_client(server_url) as (read, write):
    async with ClientSession(read, write) as session:
        # Session automatically closed on exit
        pass
```

### Timeout Configuration

```python
# Set custom timeout
import aiohttp

timeout = aiohttp.ClientTimeout(total=60)
async with sse_client(server_url, timeout=timeout) as (read, write):
    # ...
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def resilient_call():
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            return await session.call_tool("sap_authenticate", {})
```

## Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run tests
pytest

# Run specific test
pytest tests/test_sse_client.py

# Run with coverage
pytest --cov
```

### Code Quality

```bash
# Format code
black .
isort .

# Type checking
mypy .
```

## Troubleshooting

### Connection Refused

```bash
# Check if server is running
curl http://localhost:8000/sse

# Verify server URL in .env
echo $SAP_MCP_SERVER_URL
```

### Authentication Failed

```bash
# Server handles authentication
# Check server logs:
docker logs sap-mcp-server
```

### Timeout Issues

```python
# Increase timeout
import aiohttp
timeout = aiohttp.ClientTimeout(total=120)
```

## Node.js Client

For Node.js/TypeScript applications:

```bash
npm install @modelcontextprotocol/sdk
```

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const transport = new SSEClientTransport(
  new URL("http://localhost:8000/sse")
);

const client = new Client({
  name: "sap-client",
  version: "1.0.0",
}, {
  capabilities: {}
});

await client.connect(transport);

const result = await client.callTool({
  name: "sap_authenticate",
  arguments: {}
});
```

## API Reference

Full API documentation: https://sap-mcp-client.readthedocs.io

## License

MIT License - see LICENSE file for details

## Support

- Documentation: https://sap-mcp-client.readthedocs.io
- Issues: https://github.com/company/sap-mcp-client/issues
- Server Repository: https://github.com/company/sap-mcp-server

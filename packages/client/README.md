# SAP MCP Client (Refactored)

High-level Python client library for SAP MCP Server.

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Use
from sap_mcp_client import SAPMCPClient

async with SAPMCPClient() as client:
    await client.authenticate()
    order = await client.get_order("Z_ORDER_SRV", "OrderSet", "12345")
```

## 📦 Structure

```
src/sap_mcp_client/
├── client.py      # High-level API
├── session.py     # Session management
├── transports/    # Transport layers
├── types.py       # Type definitions
└── exceptions.py  # Client exceptions
```

## 🧪 Testing

```bash
pytest
```

## 📚 Documentation

See [../../docs](../../docs) for complete documentation.

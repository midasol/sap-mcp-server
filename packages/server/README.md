# SAP MCP Server (Refactored)

Python server implementing Model Context Protocol for SAP Gateway integration.

## 🚀 Quick Start

```bash
# Install
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env with your SAP credentials

# Run
python -m sap_mcp_server.transports.stdio
```

## 📦 Structure

```
src/sap_mcp_server/
├── core/          # SAP client and business logic
├── tools/         # MCP tools
├── config/        # Configuration management
├── transports/    # Transport layers (stdio, SSE)
└── utils/         # Utilities
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific tests
pytest tests/unit/
pytest tests/integration/ -m sap
```

## 📚 Documentation

See [../../docs](../../docs) for complete documentation.

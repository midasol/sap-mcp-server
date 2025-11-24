# SAP MCP Server

Production-ready MCP (Model Context Protocol) server for SAP Gateway integration with modular architecture.

## 🎯 Overview

Enterprise-grade Python server that enables AI agents and applications to interact with SAP Gateway systems through a clean, modular architecture. Built for reliability, security, and developer experience.

**Version**: 0.2.0
**Python**: 3.11+
**Status**: ✅ Production Ready

### Key Features

- 🔐 **Secure SAP Integration**: Enterprise-grade authentication and SSL/TLS support
- 🛠️ **4 Modular Tools**: Authentication, query, entity retrieval, service discovery
- 🚀 **Stdio Transport**: Production-ready MCP server
- 📊 **Structured Logging**: JSON and console formats with performance metrics
- ✅ **Validated Inputs**: Comprehensive OData and security validation
- 🧪 **Well-Tested**: 56% coverage, 44/45 tests passing (98% success rate)

## 🚀 Quick Start

### Installation

```bash
# Navigate to server package
cd packages/server

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### Configuration

```bash
# Copy environment template
cp .env.server.example .env.server

# Edit with your SAP credentials
vim .env.server
```

**Required Environment Variables**:
```bash
SAP_HOST=your-sap-host.com
SAP_PORT=443
SAP_USERNAME=your-username
SAP_PASSWORD=your-password
SAP_CLIENT=100
SAP_VERIFY_SSL=true
SAP_TIMEOUT=30
```

### Running the Server

```bash
# Using CLI command (recommended)
sap-mcp-server-stdio

# Or directly with Python
python -m sap_mcp_server.transports.stdio
```

## 📦 Package Structure

```
src/sap_mcp_server/
├── core/                    # Core SAP integration
│   ├── sap_client.py        # OData operations
│   ├── auth.py              # Authentication manager
│   └── exceptions.py        # Custom exceptions
├── config/                  # Configuration management
│   ├── settings.py          # Environment config
│   ├── loader.py            # YAML loader
│   └── schemas.py           # Pydantic models
├── protocol/                # MCP protocol
│   └── schemas.py           # Request/Response schemas
├── tools/                   # SAP tools (4 modular tools)
│   ├── base.py              # Tool base class
│   ├── auth_tool.py         # Authentication
│   ├── query_tool.py        # OData queries
│   ├── entity_tool.py       # Entity retrieval
│   └── service_tool.py      # Service discovery
├── transports/              # Transport layer
│   └── stdio.py             # Stdio transport ✅
└── utils/                   # Utilities
    ├── logger.py            # Structured logging
    └── validators.py        # Input validation
```

## 🛠️ Available Tools

### 1. sap_authenticate

Authenticate with SAP Gateway system.

**Request**:
```json
{
  "name": "sap_authenticate",
  "arguments": {}
}
```

**Response**:
```json
{
  "success": true,
  "session_id": "abc123...",
  "message": "Successfully authenticated with SAP"
}
```

### 2. sap_query

Query SAP entities with OData filters.

**Request**:
```json
{
  "name": "sap_query",
  "arguments": {
    "service": "Z_SALES_ORDER_GENAI_SRV",
    "entity_set": "zsd004Set",
    "filter": "OrderID eq '91000043'",
    "select": "OrderID,Bstnk,Kunnr",
    "top": 10
  }
}
```

### 3. sap_get_entity

Retrieve a specific entity by key.

**Request**:
```json
{
  "name": "sap_get_entity",
  "arguments": {
    "service": "Z_SALES_ORDER_GENAI_SRV",
    "entity_set": "zsd004Set",
    "entity_key": "91000043"
  }
}
```

### 4. sap_list_services

List all available SAP services.

**Request**:
```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

## 🧪 Testing

### Running Tests

```bash
# All tests with verbose output
python -m pytest -v

# With coverage report
python -m pytest --cov=sap_mcp_server --cov-report=term-missing

# HTML coverage report
python -m pytest --cov=sap_mcp_server --cov-report=html

# Specific test categories
python -m pytest -m unit          # Unit tests only
python -m pytest -m integration   # Integration tests only
python -m pytest -m sap           # SAP integration tests

# Watch mode (requires pytest-watch)
ptw -- -v
```

### Coverage Report

**Current: 56%** (Target: 70%+)

| Module | Coverage | Status |
|--------|----------|--------|
| `tools/base.py` | 100% | 🟢 Excellent |
| `protocol/schemas.py` | 100% | 🟢 Excellent |
| `tools/service_tool.py` | 88% | 🟢 Good |
| `config/settings.py` | 82% | 🟢 Good |
| `utils/validators.py` | 80% | 🟢 Good |
| `core/sap_client.py` | 45% | 🟡 Needs Work |
| `transports/stdio.py` | 30% | 🟡 Needs Work |

## 🔒 Security

### Defense in Depth

- **Input Validation**: OData syntax, SQL injection prevention
- **Authentication**: Credential validation, session management
- **Authorization**: Service access control
- **Transport Security**: SSL/TLS, certificate verification
- **Audit Logging**: Structured logs, no sensitive data

### Best Practices

1. **Credentials**: Store in `.env.server`, never commit to git
2. **SSL/TLS**: Always enable in production (`SAP_VERIFY_SSL=true`)
3. **Validation**: All inputs validated before SAP calls
4. **Logging**: Sensitive data excluded from logs
5. **Error Handling**: Generic error messages to clients

## 🛠️ Development

### Adding a New Tool

1. **Create Tool File**: `src/sap_mcp_server/tools/my_tool.py`

```python
from .base import MCPTool

class MyNewTool(MCPTool):
    @property
    def name(self) -> str:
        return "my_new_tool"

    @property
    def description(self) -> str:
        return "Description of my new tool"

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            },
            "required": ["param"]
        }

    async def execute(self, params: dict) -> dict:
        # Implementation
        return {"result": "success"}
```

2. **Register Tool**: Update `src/sap_mcp_server/tools/__init__.py`

```python
from .my_tool import MyNewTool

# Add to registry
tool_registry.register(MyNewTool())
```

3. **Add Tests**: `tests/unit/test_my_tool.py`



## 📚 Documentation

- **[Configuration Guide](../../docs/guides/configuration.md)**: YAML and environment setup
- **[Deployment Guide](../../docs/guides/deployment.md)**: Production deployment
- **[Architecture](../../docs/architecture/server.md)**: System architecture details

## 📝 License

MIT License - see [LICENSE](../../LICENSE) file for details.

## 🆘 Support

- **Issues**: Create an issue in the main repository
- **Documentation**: See `../../docs/` directory
- **Examples**: Check `../client/examples/` directory

# SAP MCP Project Structure

This repository contains two separate packages for SAP MCP integration:

## Repository Structure

```
sap-mcp/
├── sap-mcp-server/          # Server package (deployed separately)
│   ├── src/
│   │   └── sap_mcp/         # Server source code
│   │       ├── sap/         # SAP Gateway client
│   │       ├── protocol/    # MCP protocol implementation
│   │       ├── config/      # Configuration management
│   │       │   ├── settings.py      # Server settings
│   │       │   ├── schemas.py       # YAML configuration Pydantic models
│   │       │   └── services_loader.py  # YAML configuration loader
│   │       ├── sse_server.py   # SSE server (production)
│   │       └── stdio_server.py # Stdio server (development)
│   ├── config/              # YAML configuration files
│   │   ├── services.yaml         # Default service configuration
│   │   └── services.yaml.example # Extended configuration examples
│   ├── pyproject.toml       # Server dependencies
│   ├── .env.example         # Server environment template
│   ├── DEPLOYMENT.md        # Deployment guide
│   ├── CONFIGURATION_GUIDE.md   # YAML configuration reference
│   ├── REFACTORING_SUMMARY.md   # Refactoring documentation
│   ├── ARCHITECTURE.md      # Architecture documentation
│   └── README.md            # Server documentation
│
├── sap-mcp-client/          # Client package (used by applications)
│   ├── examples/
│   │   ├── sse_client.py    # SSE client example
│   │   └── stdio_client.py  # Stdio client example
│   ├── pyproject.toml       # Client dependencies
│   ├── .env.example         # Client environment template
│   └── README.md            # Client documentation
│
├── PROJECT_STRUCTURE.md     # This file
└── README.md                # Main project documentation

```

## Package Purpose

### sap-mcp-server

**Purpose**: Standalone MCP server for SAP Gateway integration

**Deployment**:
- Production: Docker container, Kubernetes pod
- Development: Local Python process

**Dependencies**:
- MCP server SDK
- FastAPI, Uvicorn (HTTP/SSE)
- SAP Gateway client (aiohttp, xmltodict)
- Full server framework

**Entry Points**:
- `sap-mcp-server`: SSE server (production)
- `sap-mcp-server-stdio`: Stdio server (development)

### sap-mcp-client

**Purpose**: Lightweight client library for applications

**Usage**:
- Python applications
- Jupyter notebooks
- AI/ML pipelines
- Integration scripts

**Dependencies**:
- MCP client SDK only
- Minimal dependencies (mcp, aiohttp)
- No server components

**Usage Pattern**:
```python
from mcp import ClientSession
from mcp.client.sse import sse_client

async with sse_client(server_url) as (read, write):
    async with ClientSession(read, write) as session:
        result = await session.call_tool("sap_get_entity", {...})
```

## Development Workflow

### Server Development

```bash
cd sap-mcp-server

# Setup
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Configure
cp .env.example .env
vim .env

# Run
python -m sap_mcp.sse_server

# Test
pytest
```

### Client Development

```bash
cd sap-mcp-client

# Setup
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Configure
cp .env.example .env
vim .env

# Run examples
python examples/sse_client.py

# Test
pytest
```

## Deployment Scenarios

### Scenario 1: Production Deployment

```
┌─────────────────────────┐
│ Kubernetes Cluster      │
│                         │
│  ┌──────────────────┐   │
│  │ sap-mcp-server   │   │
│  │ (3 replicas)     │   │
│  └────────┬─────────┘   │
│           │             │
└───────────┼─────────────┘
            │ HTTP/SSE
    ┌───────┼───────┐
    │       │       │
    ▼       ▼       ▼
┌────────┐ ┌────────┐ ┌────────┐
│ App 1  │ │ App 2  │ │ App 3  │
│(client)│ │(client)│ │(client)│
└────────┘ └────────┘ └────────┘
```

**Server**: Deployed in Kubernetes
**Clients**: Installed via pip in each application

### Scenario 2: Development Setup

```
Terminal 1:          Terminal 2:
┌──────────────┐    ┌──────────────┐
│ Server       │    │ Client       │
│ python -m    │    │ python       │
│ sap_mcp.     │◄───┤ client.py    │
│ sse_server   │HTTP│              │
└──────────────┘    └──────────────┘
```

### Scenario 3: Stdio Mode (Testing)

```
┌──────────────────────────┐
│ Client Process           │
│  ┌────────────────────┐  │
│  │ MCP Client         │  │
│  │  ├─ stdio ────────┐│  │
│  │  │                ││  │
│  │  │  ┌──────────┐  ││  │
│  │  └─►│  Server  │  ││  │
│  │     │ (subprocess)││  │
│  │     └──────────┘  ││  │
│  └────────────────────┘  │
└──────────────────────────┘
```

## Installation

### Server Installation

```bash
# From source
cd sap-mcp-server
pip install -e .

# Or build wheel
python -m build
pip install dist/sap_mcp_server-*.whl
```

### Client Installation

```bash
# From source
cd sap-mcp-client
pip install -e .

# Or build wheel
python -m build
pip install dist/sap_mcp_client-*.whl

# Or from PyPI (when published)
pip install sap-mcp-client
```

## Configuration

### YAML Service Configuration

The server uses a YAML-based configuration system to define SAP services and entities, making it completely generic and service-agnostic.

**Configuration Files**:
- `config/services.yaml`: Default service configuration
- `config/services.yaml.example`: Extended examples with multiple services

**Key Components**:

#### 1. Configuration Schemas (`src/sap_mcp/config/schemas.py`)
Pydantic models for type-safe YAML validation:
- `EntityConfig`: Entity set definitions with key fields and navigation
- `ServiceConfig`: Service metadata with OData version and entities
- `GatewayConfig`: Gateway URL patterns and metadata endpoints
- `ServicesYAMLConfig`: Complete configuration structure

#### 2. Configuration Loader (`src/sap_mcp/config/services_loader.py`)
YAML loading system with:
- Singleton pattern for efficient caching
- Path security validation (prevents directory traversal)
- Automatic fallback to default configuration
- Runtime reload capability

#### 3. Configuration Priority
1. **Custom Path**: `MCP_SERVICES_CONFIG_PATH` environment variable
2. **Default Location**: `config/services.yaml` (relative to package)
3. **Fallback**: Hardcoded default configuration

**Example YAML Configuration**:
```yaml
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"

services:
  - id: Z_SALES_ORDER_SRV
    name: "Sales Order Service"
    path: "/SAP/Z_SALES_ORDER_SRV"
    version: v2
    entities:
      - name: SalesOrderSet
        key_field: Vbeln
        default_select: [Vbeln, Erdat, Netwr]
```

See [CONFIGURATION_GUIDE.md](./sap-mcp-server/CONFIGURATION_GUIDE.md) for complete documentation.

### Server Environment Variables

```bash
# SAP Connection
SAP_HOST=sap-gateway.company.com
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=sapuser
SAP_PASSWORD=******

# Server Settings
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_LOG_LEVEL=INFO

# Optional: Custom YAML configuration path
MCP_SERVICES_CONFIG_PATH=/path/to/custom/services.yaml
```

### Client Environment Variables

```bash
# Server Connection
SAP_MCP_SERVER_URL=http://sap-mcp-server:8000/sse

# Client Settings (optional)
MCP_CLIENT_TIMEOUT=30
MCP_CLIENT_RETRY_ATTEMPTS=3
```

## Security

### Server Security

- Environment variables for credentials
- No credentials in code or config files
- SSL/TLS for production deployments
- API authentication on SSE endpoint
- Network security (VPC, firewall rules)

### Client Security

- Server URL configuration only
- No SAP credentials needed
- Server handles all authentication
- Encrypted transport (HTTPS)

## Testing

### Server Testing

```bash
cd sap-mcp-server
pytest tests/

# Unit tests
pytest tests/unit/

# Integration tests (requires SAP)
pytest tests/integration/ -m sap
```

### Client Testing

```bash
cd sap-mcp-client
pytest tests/

# Mock server tests
pytest tests/test_client.py

# Integration tests (requires running server)
pytest tests/integration/
```

## Publishing

### Build Packages

```bash
# Build server package
cd sap-mcp-server
python -m build

# Build client package
cd sap-mcp-client
python -m build
```

### Publish to PyPI

```bash
# Server
cd sap-mcp-server
twine upload dist/*

# Client
cd sap-mcp-client
twine upload dist/*
```

## Migration Guide

If you have existing code using the monolithic package:

### Before (Monolithic)

```python
# Had to install everything
pip install sap-mcp

from sap_mcp.client import SAPClient
```

### After (Separated)

**For server deployment:**
```bash
pip install sap-mcp-server
python -m sap_mcp.sse_server
```

**For client applications:**
```bash
pip install sap-mcp-client
```

```python
from mcp import ClientSession
from mcp.client.sse import sse_client

async with sse_client("http://server:8000/sse") as (r, w):
    async with ClientSession(r, w) as session:
        result = await session.call_tool("sap_authenticate", {})
```

## Support

- Server Issues: https://github.com/company/sap-mcp-server/issues
- Client Issues: https://github.com/company/sap-mcp-client/issues
- Documentation: https://sap-mcp.readthedocs.io

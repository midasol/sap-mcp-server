# SAP MCP Server

SAP Gateway Model Context Protocol (MCP) Server - Standalone server for SAP integration via MCP.

## Overview

SAP MCP Server is a production-ready MCP server that provides SAP Gateway OData integration through the Model Context Protocol. It runs as a standalone HTTP/SSE server that can be deployed independently and accessed by multiple clients.

## Features

- ✅ **SSE Transport**: HTTP-based Server-Sent Events for production deployment
- ✅ **Stdio Transport**: Standard I/O for development and testing
- ✅ **SAP Gateway Integration**: Full OData v2/v4 support
- ✅ **YAML Configuration**: Generic, service-agnostic design with YAML-based configuration
- ✅ **Authentication**: Secure SAP credential management
- ✅ **Production Ready**: Docker, Kubernetes, and cloud deployment support
- ✅ **Monitoring**: Built-in health checks and metrics

## Quick Start

### Installation

```bash
# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Configuration

#### 1. Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
vim .env
```

Required environment variables:

```bash
# SAP Connection
SAP_HOST=your-sap-server.com
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=your_username
SAP_PASSWORD=your_password

# Server Configuration
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_LOG_LEVEL=INFO

# Optional: Custom services configuration path
MCP_SERVICES_CONFIG_PATH=config/services.yaml
```

#### 2. Service Configuration (YAML)

The server uses YAML configuration to define SAP services and entities. This makes it completely generic and adaptable to any SAP OData service.

**Create/Edit** `config/services.yaml`:

```yaml
# Gateway URL configuration
gateway:
  base_url_pattern: "https://{host}:{port}/sap/opu/odata"

# SAP OData Services
services:
  - id: Z_SALES_ORDER_SRV
    name: "Sales Order Service"
    path: "/SAP/Z_SALES_ORDER_SRV"
    version: v2
    entities:
      - name: SalesOrderSet
        key_field: Vbeln
        description: "Sales orders"
        default_select:
          - Vbeln
          - Erdat
          - Netwr
```

**See [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) for complete YAML configuration documentation.**

### Running the Server

**SSE Mode (Production):**

```bash
# Using Python module
python -m sap_mcp.sse_server

# Using entry point
sap-mcp-server

# With custom port
MCP_PORT=9000 sap-mcp-server
```

**Stdio Mode (Development):**

```bash
python -m sap_mcp.stdio_server
```

### Docker Deployment

```bash
# Build image
docker build -t sap-mcp-server .

# Run container
docker run -d \
  --name sap-mcp \
  -p 8000:8000 \
  --env-file .env \
  sap-mcp-server
```

### Docker Compose

```yaml
version: '3.8'
services:
  sap-mcp:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Architecture

```
┌─────────────────────────────────────┐
│  SAP MCP Server (SSE)               │
│  http://server:8000/sse             │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  MCP Protocol Layer         │   │
│  └─────────────┬───────────────┘   │
│                │                    │
│  ┌─────────────▼───────────────┐   │
│  │  SAP Gateway Client          │   │
│  │  - Authentication            │   │
│  │  - OData Operations          │   │
│  │  - Connection Pooling        │   │
│  └─────────────┬───────────────┘   │
│                │                    │
└────────────────┼────────────────────┘
                 │ OData HTTP
                 ▼
        ┌────────────────┐
        │  SAP Gateway   │
        │  (NetWeaver)   │
        └────────────────┘
```

## Available Tools

### `sap_list_services`

List all available SAP OData services configured in `services.yaml`.

```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

**Response**:
```json
{
  "success": true,
  "count": 2,
  "services": [
    {
      "id": "Z_SALES_ORDER_SRV",
      "name": "Sales Order Service",
      "path": "/SAP/Z_SALES_ORDER_SRV",
      "version": "v2",
      "entities": [...]
    }
  ]
}
```

### `sap_authenticate`

Authenticate with SAP Gateway and establish a session.

```json
{
  "name": "sap_authenticate",
  "arguments": {}
}
```

### `sap_get_entity`

Retrieve a specific entity by key. Service and entity must be defined in `services.yaml`.

```json
{
  "name": "sap_get_entity",
  "arguments": {
    "service": "Z_SALES_ORDER_SRV",
    "entity_set": "SalesOrderSet",
    "entity_key": "12345"
  }
}
```

**Note**: The tool validates that the service and entity exist in your YAML configuration and provides helpful error messages if not found.

### `sap_query`

Query entities with filters and pagination.

```json
{
  "name": "sap_query",
  "arguments": {
    "service": "Z_SALES_ORDER_SRV",
    "entity_set": "SalesOrderSet",
    "filter": "Status eq 'OPEN'",
    "top": 50,
    "skip": 0
  }
}
```

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed production deployment guides including:

- Kubernetes deployment
- Load balancer configuration
- SSL/TLS setup
- Security best practices
- Monitoring and logging
- High availability setup

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_sap_client.py

# Run integration tests (requires SAP connection)
pytest -m integration
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/

# Security scan
bandit -r src/
```

## Configuration Reference

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SAP_HOST` | SAP Gateway hostname | - | Yes |
| `SAP_PORT` | SAP Gateway HTTPS port | `44300` | Yes |
| `SAP_CLIENT` | SAP client number | `100` | Yes |
| `SAP_USERNAME` | SAP username | - | Yes |
| `SAP_PASSWORD` | SAP password | - | Yes |
| `SAP_VERIFY_SSL` | Verify SSL certificates | `false` | No |
| `SAP_TIMEOUT` | Request timeout (seconds) | `30` | No |
| `SAP_RETRY_ATTEMPTS` | Number of retries | `3` | No |
| `MCP_HOST` | Server bind address | `0.0.0.0` | No |
| `MCP_PORT` | Server port | `8000` | No |
| `MCP_LOG_LEVEL` | Logging level | `INFO` | No |
| `MCP_SERVICES_CONFIG_PATH` | Path to services.yaml | `config/services.yaml` | No |

### Service Configuration (YAML)

See [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) for complete documentation on:
- YAML schema and structure
- How to add new services and entities
- Gateway URL pattern configuration
- Configuration best practices
- Troubleshooting and validation

## Troubleshooting

### Server Won't Start

```bash
# Check port availability
netstat -tuln | grep 8000

# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.environ.get('SAP_HOST'))"

# Check logs
tail -f logs/sap-mcp-server.log
```

### SAP Connection Failed

```bash
# Test SAP connectivity
curl -k https://${SAP_HOST}:${SAP_PORT}/sap/opu/odata/sap/

# Verify credentials
python -m sap_mcp.sap.auth
```

### SSE Connection Issues

```bash
# Test SSE endpoint
curl -N http://localhost:8000/sse

# Check server health
curl http://localhost:8000/health
```

## Security

- **Credentials**: Never commit `.env` files with real credentials
- **SSL/TLS**: Use HTTPS in production with valid certificates
- **Authentication**: Implement API authentication for SSE endpoint
- **Network**: Use VPC/private networks for SAP connections
- **Monitoring**: Enable audit logging and intrusion detection

## License

MIT License - see LICENSE file for details

## Support

- Documentation: https://sap-mcp-server.readthedocs.io
- Issues: https://github.com/company/sap-mcp-server/issues
- Discussions: https://github.com/company/sap-mcp-server/discussions

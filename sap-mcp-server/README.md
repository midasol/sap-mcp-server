# SAP MCP Server

SAP Gateway Model Context Protocol (MCP) Server - Stdio-based server for SAP integration via MCP.

## Overview

SAP MCP Server is a stdio-based MCP server that provides SAP Gateway OData integration through the Model Context Protocol. It uses standard input/output for communication, making it ideal for local development, Claude Desktop integration, and automated workflows.

## Features

- ✅ **Stdio Transport**: Standard I/O communication for simple, reliable operation
- ✅ **SAP Gateway Integration**: Full OData v2/v4 support
- ✅ **YAML Configuration**: Generic, service-agnostic design with YAML-based configuration
- ✅ **Authentication**: Secure SAP credential management
- ✅ **Claude Desktop Integration**: Direct integration with Claude Desktop
- ✅ **Easy Setup**: No network configuration or port management needed

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

⚠️ **중요**: `.env.server` 파일에 **실제 SAP 서버 정보**를 입력해야 합니다.

```bash
# Edit .env.server with your actual SAP credentials
vim .env.server
```

**Required environment variables:**

```bash
# SAP Connection
SAP_HOST=actual-sap-server.company.com  # ← 실제 SAP 서버 주소
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=actual_username            # ← 실제 사용자명
SAP_PASSWORD=actual_password            # ← 실제 비밀번호

# Connection Settings
SAP_VERIFY_SSL=false
SAP_TIMEOUT=30
SAP_RETRY_ATTEMPTS=3

# Optional: Custom services configuration path
MCP_SERVICES_CONFIG_PATH=config/services.yaml
```

**Verify configuration:**

```bash
python test_env_loading.py
```

Expected output when configured correctly:
```
✅ All environment variables are set with real values
✅ SAPConnectionConfig created successfully!
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

**Stdio Mode:**

```bash
# Using Python module (recommended)
python -m sap_mcp.stdio_server

# Using entry point
sap-mcp-server
```

The server will:
1. Load environment variables from `.env.server`
2. Initialize SAP connection
3. Start listening on stdin/stdout for MCP protocol messages

**Note**: Stdio mode is designed to be spawned by MCP clients. The server will wait for JSON-RPC messages on stdin and respond on stdout.

### Claude Desktop Integration

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sap-mcp": {
      "command": "python",
      "args": ["-m", "sap_mcp.stdio_server"],
      "env": {
        "SAP_HOST": "actual-sap-server.company.com",
        "SAP_PORT": "44300",
        "SAP_CLIENT": "100",
        "SAP_USERNAME": "actual_username",
        "SAP_PASSWORD": "actual_password",
        "SAP_VERIFY_SSL": "false"
      }
    }
  }
}
```

Or use environment file reference:
```json
{
  "mcpServers": {
    "sap-mcp": {
      "command": "python",
      "args": ["-m", "sap_mcp.stdio_server"]
    }
  }
}
```

Claude Desktop will automatically spawn the server and communicate via stdio.

## Architecture

```
┌─────────────────────────────────────┐
│  MCP Client (Claude Desktop, etc)   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  MCP Client Library         │   │
│  └─────────────┬───────────────┘   │
└────────────────┼────────────────────┘
                 │ stdin/stdout
                 │ (JSON-RPC)
┌────────────────▼────────────────────┐
│  SAP MCP Server (Stdio)             │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  MCP Protocol Layer         │   │
│  │  - Tool Registration        │   │
│  │  - Message Handling         │   │
│  └─────────────┬───────────────┘   │
│                │                    │
│  ┌─────────────▼───────────────┐   │
│  │  SAP Gateway Client          │   │
│  │  - Authentication            │   │
│  │  - OData Operations          │   │
│  │  - Error Handling            │   │
│  └─────────────┬───────────────┘   │
│                │                    │
└────────────────┼────────────────────┘
                 │ OData HTTPS
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

## Client Examples

Client examples are available in the `sap-mcp-client` package:

- **stdio_client.py**: Basic stdio client that spawns the server
- **order_inquiry_chatbot.py**: Interactive chatbot for order inquiries
- **genai-example.py**: GenAI integration example

See `../sap-mcp-client/examples/README.md` for detailed usage instructions.

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

### Authentication Failed - Validation Errors

**Error:**
```
Authentication failed: 3 validation errors for SAPConnectionConfig
  host / username / password Field required
```

**Cause:** `.env.server` contains placeholder values or environment variables not loaded

**Solution:**

1. Run the test script:
   ```bash
   python test_env_loading.py
   ```

2. If placeholder values detected, edit `.env.server`:
   ```bash
   vim .env.server
   ```

3. Replace placeholders with actual values:
   - ❌ `SAP_HOST=your-sap-server.com` (placeholder)
   - ✅ `SAP_HOST=actual-server.company.com` (real value)

4. Verify configuration again:
   ```bash
   python test_env_loading.py
   ```

### ModuleNotFoundError: No module named 'sap_mcp'

**Cause:** Server package not installed

**Solution:**
```bash
pip install -e .
```

### SAP Connection Failed

**Cause:** Network connectivity or credential issues

**Solution:**

1. Test SAP connectivity:
   ```bash
   curl -k https://${SAP_HOST}:${SAP_PORT}/sap/opu/odata/sap/
   ```

2. Verify credentials in `.env.server`

3. Check SSL verification setting:
   ```bash
   # For development with self-signed certificates
   SAP_VERIFY_SSL=false

   # For production with valid certificates
   SAP_VERIFY_SSL=true
   ```

### Service or Entity Not Found

**Error:**
```
Service 'Z_SALES_ORDER_SRV' not found in configuration
```

**Cause:** Service not defined in `config/services.yaml`

**Solution:**

1. Check available services:
   ```bash
   cat config/services.yaml
   ```

2. Add the service to `services.yaml`:
   ```yaml
   services:
     - id: Z_SALES_ORDER_SRV
       name: "Sales Order Service"
       path: "/SAP/Z_SALES_ORDER_SRV"
       version: v2
       entities:
         - name: SalesOrderSet
           key_field: Vbeln
   ```

3. See [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) for detailed YAML configuration

## Security

- **Credentials**: Never commit `.env.server` or `.env` files with real credentials
  - `.env.server` is gitignored by default
  - Use `.env.server.example` as a template
- **SSL/TLS**:
  - Use `SAP_VERIFY_SSL=true` in production
  - Only use `SAP_VERIFY_SSL=false` for development with self-signed certificates
- **Environment Variables**:
  - In Claude Desktop, credentials are stored in the config file
  - Ensure config file has appropriate permissions (600)
- **Network**: Use VPN or private networks for SAP connections
- **Monitoring**: Enable audit logging for SAP operations

## License

MIT License - see LICENSE file for details

## Support

- Documentation: https://sap-mcp-server.readthedocs.io
- Issues: https://github.com/company/sap-mcp-server/issues
- Discussions: https://github.com/company/sap-mcp-server/discussions

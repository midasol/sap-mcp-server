# SAP MCP Server - Installation & Usage Guide

## Overview

SAP MCP Server is a stdio-based MCP server for SAP Gateway integration. It communicates via standard input/output, making it ideal for:

- **Local Development**: Direct integration with MCP clients
- **Claude Desktop**: Native Claude Desktop integration
- **Automated Workflows**: CI/CD pipelines and automation scripts
- **Command-Line Tools**: Interactive CLI applications

## Installation

### Prerequisites

- Python 3.11 or higher
- SAP Gateway access credentials
- Network connectivity to SAP server

### 1. Install Package

```bash
cd sap-mcp-server
pip install -e .
```

### 2. Configure SAP Credentials

⚠️ **Important**: Edit `.env.server` with your actual SAP credentials.

```bash
vim .env.server
```

```bash
# SAP Gateway Connection
SAP_HOST=actual-sap-server.company.com  # ← Real SAP server
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=actual_username            # ← Real username
SAP_PASSWORD=actual_password            # ← Real password

# Connection Settings
SAP_VERIFY_SSL=false
SAP_TIMEOUT=30
SAP_RETRY_ATTEMPTS=3
```

### 3. Verify Configuration

```bash
python test_env_loading.py
```

Expected output:
```
✅ All environment variables are set with real values
✅ SAPConnectionConfig created successfully!
```

## Usage Modes

### 1. Claude Desktop Integration

Add to Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sap-mcp": {
      "command": "python",
      "args": ["-m", "sap_mcp_server.transports.stdio"],
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

Restart Claude Desktop to activate the server.

### 2. Python Client Integration

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp_server.transports.stdio"],
        env=None  # Uses .env.server file
    )

    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            # Call SAP tools
            result = await session.call_tool(
                "sap_authenticate",
                arguments={}
            )
            print(result)

asyncio.run(main())
```

### 3. Direct Server Execution

For testing or debugging:

```bash
# Using Python module
python -m sap_mcp_server.transports.stdio

# Using entry point
sap-mcp-server
```

The server will wait for JSON-RPC messages on stdin and respond on stdout.

## Service Configuration

### YAML Configuration

Edit `config/services.yaml` to define SAP services:

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
        description: "Sales orders"
        default_select:
          - Vbeln
          - Erdat
          - Netwr
```

See [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) for detailed configuration options.

## Available Tools

### 1. `sap_list_services`
List all configured SAP services.

```json
{
  "name": "sap_list_services",
  "arguments": {}
}
```

### 2. `sap_authenticate`
Authenticate with SAP Gateway.

```json
{
  "name": "sap_authenticate",
  "arguments": {}
}
```

### 3. `sap_get_entity`
Retrieve specific entity by key.

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

### 4. `sap_query`
Query entities with filters.

```json
{
  "name": "sap_query",
  "arguments": {
    "service": "Z_SALES_ORDER_SRV",
    "entity_set": "SalesOrderSet",
    "filter": "Status eq 'OPEN'",
    "top": 50
  }
}
```

## Troubleshooting

### Authentication Failed

**Error:**
```
Authentication failed: 3 validation errors for SAPConnectionConfig
  host / username / password Field required
```

**Solution:**

1. Run test script:
   ```bash
   python test_env_loading.py
   ```

2. Edit `.env.server` with actual credentials

3. Verify configuration again

### Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'sap_mcp'
```

**Solution:**
```bash
cd sap-mcp-server
pip install -e .
```

### SAP Connection Failed

**Error:**
```
SAP connection error: Connection refused
```

**Solution:**

1. Test SAP connectivity:
   ```bash
   curl -k https://${SAP_HOST}:${SAP_PORT}/sap/opu/odata/sap/
   ```

2. Verify credentials in `.env.server`

3. Check SSL verification setting

### Service Not Found

**Error:**
```
Service 'Z_SALES_ORDER_SRV' not found in configuration
```

**Solution:**

Add service to `config/services.yaml`:

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

## Security Best Practices

### Credential Management

- **Never commit** `.env.server` or `.env` files
- Use `.env.server.example` as template
- Set appropriate file permissions: `chmod 600 .env.server`

### Claude Desktop Security

- Credentials stored in Claude Desktop config file
- Ensure config file has restricted permissions: `chmod 600 claude_desktop_config.json`
- Consider using environment variables instead of inline credentials

### SAP Connection Security

- **Production**: Use `SAP_VERIFY_SSL=true` with valid certificates
- **Development**: `SAP_VERIFY_SSL=false` only for self-signed certificates
- Use VPN or private network for SAP connections
- Monitor SAP audit logs for suspicious activity

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test
pytest tests/test_sap_client.py
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

## References

- [Architecture Documentation](./ARCHITECTURE.md)
- [Configuration Guide](./CONFIGURATION_GUIDE.md)
- [Client Examples](../sap-mcp-client/examples/README.md)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [SAP Gateway Documentation](https://help.sap.com/docs/ABAP_PLATFORM/68bf513362174d54b58cddec28794093/3a8e3e2d21d84af9a92c00bd97a99433.html)

# SAP Gateway MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with SAP Gateway services, enabling AI agents and applications to interact with SAP systems through standardized, secure, and efficient APIs.

## 🚀 Features

- **MCP Protocol Compliance**: Full Model Context Protocol support for AI agent integration
- **SAP Gateway Integration**: Native OData v2/v4 support with CSRF authentication
- **Cloud-Native**: Ready for deployment on Cloud Run, Docker, or traditional VMs
- **Security First**: Enterprise-grade security with encrypted credentials and audit logging
- **Production Ready**: Comprehensive monitoring, health checks, and error handling
- **Extensible**: Plugin architecture for custom SAP services and operations

## 🛠️ Available Tools

The MCP server provides the following tools for SAP integration:

### Authentication
- `sap_authenticate`: Establish authenticated sessions with SAP Gateway

### Data Operations
- `sap_query`: Execute OData queries to retrieve SAP data (with filtering, selection, pagination)

### Discovery
- `sap_list_services`: Discover available OData services

### Planned Tools
- `sap_create_order`: Create sales orders in SAP
- `sap_get_metadata`: Retrieve service metadata and schemas

## 📋 Prerequisites

- Python 3.11+
- SAP Gateway system with OData services
- Valid SAP credentials
- Docker (for containerized deployment)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/company/sap-mcp.git
cd sap-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
vi .env
```

Required environment variables:
```bash
SAP_HOST=your-sap-server.com
SAP_USERNAME=your-username
SAP_PASSWORD=your-password
```

### 3. Run the Server

#### As MCP Stdio Server (for MCP clients like Claude Desktop)

```bash
python -m sap_mcp.stdio_server
```

#### As HTTP Server (for REST API access)

```bash
# Development mode
python -m sap_mcp.server

# Or with uvicorn directly
uvicorn sap_mcp.protocol.server:get_app --factory --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the Connection

```bash
# Health check
curl http://localhost:8000/health

# List available tools
curl http://localhost:8000/tools
```

## 🐳 Docker Deployment

### Local Docker

```bash
# Build image
docker build -t sap-mcp-server .

# Run container
docker run -d \
  --name sap-mcp-server \
  -p 8000:8000 \
  --env-file .env \
  sap-mcp-server
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# With monitoring stack
docker-compose --profile monitoring up -d

# View logs
docker-compose logs -f sap-mcp-server
```

## ☁️ Cloud Deployment

### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/sap-mcp-server
gcloud run deploy sap-mcp-server \
  --image gcr.io/PROJECT_ID/sap-mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SAP_HOST=your-sap-server.com
```

### VM Deployment

```bash
# Install on Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# Setup service
sudo cp deployment/systemd/sap-mcp.service /etc/systemd/system/
sudo systemctl enable sap-mcp
sudo systemctl start sap-mcp
```

## 📚 Usage Examples

### MCP Client (stdio)

```python
import asyncio
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp import StdioServerParameters

async def main():
    # Configure stdio server connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sap_mcp.stdio_server"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Authenticate with SAP
            auth_result = await session.call_tool("sap_authenticate", {
                "host": "sap.company.com",
                "username": "user",
                "password": "pass"
            })
            print(f"Auth result: {auth_result}")

            # Query SAP data
            result = await session.call_tool("sap_query", {
                "service": "Z_SALES_ORDER_GENAI_SRV",
                "entity_set": "zsd004Set",
                "filter": "Auart eq 'OR'"
            })
            print(f"Query result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### cURL Examples

```bash
# Authenticate
curl -X POST http://localhost:8000/tools/sap_authenticate \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"host\": \"sap.company.com\",
    \"username\": \"user\",
    \"password\": \"pass\"
  }'

# Create sales order
curl -X POST http://localhost:8000/tools/sap_create_order \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"order_data\": {
      \"Auart\": \"OR\",
      \"Vkorg\": \"1000\",
      \"Vtweg\": \"10\",
      \"Spart\": \"00\",
      \"Kunnr\": \"100001\"
    }
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SAP_HOST` | SAP server hostname | - | ✅ |
| `SAP_PORT` | SAP server port | 44300 | ❌ |
| `SAP_USERNAME` | SAP username | - | ✅ |
| `SAP_PASSWORD` | SAP password | - | ✅ |
| `SAP_CLIENT` | SAP client number | 100 | ❌ |
| `MCP_PORT` | Server port | 8000 | ❌ |
| `LOG_LEVEL` | Logging level | INFO | ❌ |

### Service Configuration

Custom SAP services can be configured in `config/services.yaml`:

```yaml
services:
  MY_CUSTOM_SERVICE:
    name: \"MY_CUSTOM_SERVICE\"
    path: \"/sap/opu/odata/SAP/MY_CUSTOM_SERVICE\"
    version: \"v2\"
    entities:
      - \"CustomEntitySet\"
    custom_headers:
      \"Custom-Header\": \"Value\"
```

## 📊 Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Detailed health with dependencies
curl http://localhost:8000/health/detailed
```

### Metrics

Prometheus metrics available at `/metrics`:

- `sap_mcp_requests_total`: Total requests by tool and status
- `sap_mcp_request_duration_seconds`: Request duration histogram
- `sap_mcp_active_connections`: Active SAP connections
- `sap_mcp_active_sessions`: Active SAP sessions

### Logging

Structured JSON logging with correlation IDs:

```json
{
  \"timestamp\": \"2024-01-15T10:30:00Z\",
  \"level\": \"INFO\",
  \"correlation_id\": \"req-123\",
  \"tool\": \"sap_create_order\",
  \"duration_ms\": 1250,
  \"status\": \"success\"
}
```

## 🧪 Testing

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=sap_mcp --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m e2e           # End-to-end tests only
```

## 🔒 Security

### Best Practices

- Store credentials in environment variables or secure secret managers
- Enable SSL/TLS verification in production
- Use strong encryption keys for sensitive data
- Implement proper network security groups
- Enable audit logging for compliance
- Regularly update dependencies

### Security Features

- CSRF token-based authentication
- Request rate limiting
- Session timeout management
- Encrypted credential storage
- Comprehensive audit logging
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/ tests/
isort src/ tests/

# Run linting
flake8 src/ tests/
mypy src/

# Run security scan
bandit -r src/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](https://sap-mcp.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/company/sap-mcp/issues)
- 💬 [Discussions](https://github.com/company/sap-mcp/discussions)
- 📧 [Email Support](mailto:sap-mcp@company.com)

## 🗺️ Roadmap

- [ ] Additional SAP modules support (HR, Finance, etc.)
- [ ] WebSocket support for real-time updates
- [ ] GraphQL API layer
- [ ] Enhanced caching strategies
- [ ] Multi-tenant support
- [ ] Advanced monitoring and alerting

## 🙏 Acknowledgments

- [Model Context Protocol](https://github.com/anthropics/mcp) specification
- SAP OData documentation and examples
- Open source community contributions

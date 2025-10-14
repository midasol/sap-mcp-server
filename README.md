# SAP MCP - SAP Gateway Integration via Model Context Protocol

Complete MCP integration solution for SAP Gateway, providing both server and client packages for flexible deployment scenarios.

## 📦 Repository Structure

This repository contains two independent packages:

### [sap-mcp-server](./sap-mcp-server/)
Standalone MCP server for SAP Gateway integration, designed for production deployment.

**Features**:
- ✅ SSE transport for production (HTTP/Server-Sent Events)
- ✅ Stdio transport for development
- ✅ SAP Gateway OData v2/v4 support
- ✅ **YAML Configuration** - Generic, service-agnostic design
- ✅ Docker & Kubernetes ready
- ✅ Production monitoring and health checks

**Installation**:
```bash
cd sap-mcp-server
pip install -e .
```

**Quick Start**:
```bash
# Configure
cp .env.example .env
vim .env

# Run server
python -m sap_mcp.sse_server
```

### [sap-mcp-client](./sap-mcp-client/)
Lightweight Python client library for connecting to SAP MCP Server.

**Features**:
- ✅ Simple async API
- ✅ SSE and stdio transport
- ✅ Type-safe with Pydantic
- ✅ Minimal dependencies
- ✅ Example code included

**Installation**:
```bash
cd sap-mcp-client
pip install -e .
```

**Quick Start**:
```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:8000/sse") as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            result = await session.call_tool("sap_authenticate", {})
            print(result)

asyncio.run(main())
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  Production Environment             │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ Kubernetes Cluster           │   │
│  │  ┌────────────────────────┐  │   │
│  │  │ sap-mcp-server         │  │   │
│  │  │ (3 replicas)           │  │   │
│  │  │ SSE: :8000/sse         │  │   │
│  │  └─────────┬──────────────┘  │   │
│  └────────────┼─────────────────┘   │
└───────────────┼─────────────────────┘
                │ HTTP/SSE
        ┌───────┼───────┐
        │       │       │
        ▼       ▼       ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ App 1  │ │ App 2  │ │ App 3  │
    │(client)│ │(client)│ │(client)│
    └────────┘ └────────┘ └────────┘
```

**Deployment Model**:
- **Server**: Centralized deployment (Docker/Kubernetes)
- **Clients**: Distributed across applications (pip install)
- **Communication**: HTTP/SSE for production, stdio for development

## 🚀 Quick Start

### 1. Server Setup

```bash
cd sap-mcp-server

# Install
pip install -e .

# Configure SAP credentials
cp .env.example .env
vim .env  # Set SAP_HOST, SAP_USERNAME, SAP_PASSWORD

# Run server
python -m sap_mcp.sse_server
# Server running at http://localhost:8000/sse
```

### 2. Client Setup

```bash
cd sap-mcp-client

# Install
pip install -e .

# Configure server URL
cp .env.example .env
vim .env  # Set SAP_MCP_SERVER_URL

# Run example
python examples/sse_client.py
```

## 📚 Documentation

- **[Project Structure](./PROJECT_STRUCTURE.md)**: Detailed repository organization
- **[Server README](./sap-mcp-server/README.md)**: Server installation and deployment
- **[Configuration Guide](./sap-mcp-server/CONFIGURATION_GUIDE.md)**: Complete YAML configuration reference
- **[Refactoring Summary](./sap-mcp-server/REFACTORING_SUMMARY.md)**: Architecture and refactoring details
- **[Server Deployment](./sap-mcp-server/DEPLOYMENT.md)**: Production deployment guide
- **[Client README](./sap-mcp-client/README.md)**: Client usage and examples

## 🔧 Development

### Server Development

```bash
cd sap-mcp-server
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

### Client Development

```bash
cd sap-mcp-client
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

## 🐳 Docker Deployment

### Server Container

```bash
cd sap-mcp-server

# Build
docker build -t sap-mcp-server .

# Run
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
  sap-mcp-server:
    build: ./sap-mcp-server
    ports:
      - "8000:8000"
    env_file:
      - ./sap-mcp-server/.env
    restart: unless-stopped
```

## 🔒 Security

**Server Security**:
- Environment variables for SAP credentials
- SSL/TLS for production deployments
- API authentication on SSE endpoint
- Network isolation (VPC, firewall)

**Client Security**:
- No SAP credentials required
- Server URL configuration only
- HTTPS transport in production
- Server handles all authentication

## 📊 Use Cases

### Use Case 1: AI Chatbot Integration

```python
# Client application (chatbot)
from mcp import ClientSession
from mcp.client.sse import sse_client

async def get_order_status(order_id):
    async with sse_client(server_url) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            return await session.call_tool(
                "sap_get_entity",
                {
                    "service": "Z_ORDER_SRV",
                    "entity_set": "Orders",
                    "entity_key": order_id
                }
            )
```

### Use Case 2: Data Integration Pipeline

```python
# ETL job connecting to SAP
async def sync_sap_data():
    async with sse_client(server_url) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            # Query entities
            orders = await session.call_tool(
                "sap_query_entities",
                {
                    "service": "Z_ORDER_SRV",
                    "entity_set": "Orders",
                    "filter": "Status eq 'OPEN'",
                    "top": 1000
                }
            )

            # Process data...
```

### Use Case 3: Microservice SAP Gateway

```python
# FastAPI microservice
from fastapi import FastAPI
from mcp import ClientSession
from mcp.client.sse import sse_client

app = FastAPI()

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    async with sse_client(SAP_MCP_URL) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            result = await session.call_tool(
                "sap_get_entity",
                {"service": "Z_ORDER_SRV", "entity_set": "Orders", "entity_key": order_id}
            )
            return result
```

## 🧪 Testing

### Server Tests

```bash
cd sap-mcp-server

# Unit tests
pytest tests/unit/

# Integration tests (requires SAP)
pytest tests/integration/ -m sap

# All tests with coverage
pytest --cov
```

### Client Tests

```bash
cd sap-mcp-client

# Mock server tests
pytest tests/

# Integration tests (requires running server)
SAP_MCP_SERVER_URL=http://localhost:8000/sse pytest tests/integration/
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: https://sap-mcp.readthedocs.io
- **Issues**: https://github.com/company/sap-mcp/issues
- **Discussions**: https://github.com/company/sap-mcp/discussions

## 🗺️ Roadmap

- [ ] Publish packages to PyPI
- [ ] Add WebSocket transport option
- [ ] Support SAP BTP Cloud Foundry
- [ ] Add GraphQL interface
- [ ] Multi-tenant support
- [ ] Advanced caching and performance optimization
- [ ] SAP Business One integration
- [ ] SAP S/4HANA Cloud support

## 📜 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

**Built with ❤️ for SAP integration via Model Context Protocol**

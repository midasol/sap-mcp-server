# SAP MCP SSE Server Deployment Guide

## Overview

SAP MCP supports two deployment modes:

1. **Stdio Mode** (Development): Server and client run in same process
2. **SSE Mode** (Production): Server runs separately, clients connect via HTTP

## SSE Architecture

```
┌─────────────────────────────────────┐
│  SAP MCP SSE Server                 │
│  (Separate Server/Container)        │
│                                     │
│  http://server:8000/sse             │
└─────────────┬───────────────────────┘
              │ HTTP/SSE
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Client 1│ │Client 2│ │Client N│
└────────┘ └────────┘ └────────┘
```

## Server Setup

### 1. Environment Configuration

Copy `.env.example.server` to `.env.server`:

```bash
cp .env.example.server .env.server
```

Edit `.env.server`:

```bash
# SAP Gateway Connection (REQUIRED)
SAP_HOST=your-sap-server.com
SAP_PORT=44300
SAP_CLIENT=100
SAP_USERNAME=your_username
SAP_PASSWORD=your_password

# SSE Server Configuration
MCP_HOST=0.0.0.0              # Listen on all interfaces
MCP_PORT=8000                  # HTTP port
MCP_LOG_LEVEL=INFO
```

### 2. Start SSE Server

**Development:**
```bash
python -m sap_mcp.sse_server
```

**Production (with uvicorn):**
```bash
uvicorn sap_mcp.sse_server:app --host 0.0.0.0 --port 8000
```

**Docker:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

CMD ["python", "-m", "sap_mcp.sse_server"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  sap-mcp:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env.server
    restart: unless-stopped
```

### 3. Verify Server

```bash
curl http://localhost:8000/sse
```

Expected: SSE connection established

## Client Setup

### Python Client

**Install MCP client:**
```bash
pip install mcp
```

**Example client code:**
```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to SSE server
    server_url = "http://localhost:8000/sse"

    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call SAP tools
            result = await session.call_tool("sap_authenticate", {})
            print(result)

asyncio.run(main())
```

**Run test client:**
```bash
python sap-mcp-client-sse-test.py
```

### Node.js Client

**Install MCP client:**
```bash
npm install @modelcontextprotocol/sdk
```

**Example client code:**
```javascript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

async function main() {
  const transport = new SSEClientTransport(
    new URL("http://localhost:8000/sse")
  );

  const client = new Client({
    name: "sap-mcp-client",
    version: "1.0.0",
  }, {
    capabilities: {}
  });

  await client.connect(transport);

  // Call SAP tools
  const result = await client.callTool({
    name: "sap_authenticate",
    arguments: {}
  });

  console.log(result);
}

main();
```

## Production Deployment

### 1. Load Balancer Setup

```nginx
upstream sap_mcp {
    server sap-mcp-1:8000;
    server sap-mcp-2:8000;
    server sap-mcp-3:8000;
}

server {
    listen 80;
    server_name sap-mcp.company.com;

    location /sse {
        proxy_pass http://sap_mcp;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_cache off;
    }
}
```

### 2. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sap-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sap-mcp
  template:
    metadata:
      labels:
        app: sap-mcp
    spec:
      containers:
      - name: sap-mcp
        image: company/sap-mcp:latest
        ports:
        - containerPort: 8000
        env:
        - name: SAP_HOST
          valueFrom:
            secretKeyRef:
              name: sap-credentials
              key: host
        - name: SAP_USERNAME
          valueFrom:
            secretKeyRef:
              name: sap-credentials
              key: username
        - name: SAP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: sap-credentials
              key: password
---
apiVersion: v1
kind: Service
metadata:
  name: sap-mcp
spec:
  selector:
    app: sap-mcp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. Security Considerations

**HTTPS/TLS:**
```bash
# Use reverse proxy with SSL termination
# Or configure uvicorn with SSL:
uvicorn sap_mcp.sse_server:app \
  --host 0.0.0.0 \
  --port 8443 \
  --ssl-keyfile /path/to/key.pem \
  --ssl-certfile /path/to/cert.pem
```

**Authentication:**
- Add API key validation in SSE endpoint
- Use OAuth2/JWT for client authentication
- Implement rate limiting

**Network:**
- Use VPC/private network for SAP connections
- Firewall rules to restrict SSE access
- Monitor for unusual traffic patterns

## Monitoring

### Health Check

```python
# Add to sse_server.py
from starlette.routing import Route

async def health_check(request):
    return JSONResponse({"status": "healthy"})

routes = [
    Route("/sse", endpoint=handle_sse),
    Route("/health", endpoint=health_check),
]
```

### Logging

```python
# Configure structured logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics

```python
# Add Prometheus metrics
from prometheus_client import Counter, Histogram
requests_total = Counter('mcp_requests_total', 'Total MCP requests')
request_duration = Histogram('mcp_request_duration_seconds', 'Request duration')
```

## Troubleshooting

### Server not starting

```bash
# Check port availability
netstat -tuln | grep 8000

# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv('.env.server'); print(os.environ)"
```

### Client connection failed

```bash
# Test SSE endpoint
curl -N http://localhost:8000/sse

# Check server logs
tail -f logs/sap-mcp.log
```

### SAP authentication failed

```bash
# Verify SAP credentials
python -c "from sap_mcp.sap.auth import SAPAuthenticator; import asyncio; asyncio.run(SAPAuthenticator().authenticate())"
```

## Migration from Stdio to SSE

1. Keep stdio server for development
2. Deploy SSE server to staging
3. Test client connections
4. Update production clients to use SSE
5. Monitor and validate

## References

- [MCP SSE Documentation](https://modelcontextprotocol.io/docs/concepts/transports#sse)
- [SAP MCP Architecture](./ARCHITECTURE.md)
- [Client Examples](./examples/)

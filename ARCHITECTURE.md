# SAP Gateway MCP Server - Architecture Documentation

## Overview

The SAP Gateway MCP Server provides dual transport support (stdio and HTTP) for integrating AI assistants with SAP systems through the Model Context Protocol (MCP).

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Clients                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Claude       │  │ Custom MCP   │  │ HTTP/REST    │      │
│  │ Desktop      │  │ Client       │  │ Client       │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │ stdio            │ stdio            │ HTTP
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────────┐
│              SAP MCP Server Application                      │
│  ┌──────────────────────┐  ┌───────────────────────────┐   │
│  │  stdio_server.py     │  │  protocol/server.py       │   │
│  │  (MCP SDK)           │  │  (FastAPI)                │   │
│  └──────────┬───────────┘  └────────────┬──────────────┘   │
│             │                           │                   │
│             └───────────┬───────────────┘                   │
│                         │                                   │
│              ┌──────────▼──────────┐                        │
│              │   Tool Registry     │                        │
│              │  (protocol/tools)   │                        │
│              └──────────┬──────────┘                        │
│                         │                                   │
│              ┌──────────▼──────────┐                        │
│              │   SAP Tools         │                        │
│              │  (sap/tools.py)     │                        │
│              └──────────┬──────────┘                        │
│                         │                                   │
│              ┌──────────▼──────────┐                        │
│              │   SAP Client        │                        │
│              │  (sap/client.py)    │                        │
│              └──────────┬──────────┘                        │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          │ HTTPS/OData
                          │
                ┌─────────▼──────────┐
                │   SAP Gateway      │
                │   System           │
                └────────────────────┘
```

## Components

### 1. MCP Stdio Server (`stdio_server.py`)

Implements MCP protocol over stdio transport for integration with MCP clients.

**Features**:
- Native MCP SDK integration
- Tool registration and discovery
- Stdio message handling
- Session lifecycle management

**Used By**: Claude Desktop, custom MCP clients

### 2. HTTP Server (`protocol/server.py`)

FastAPI-based REST API for HTTP clients.

**Endpoints**:
- `GET /health` - Basic health status
- `GET /tools` - List available tools
- `POST /tools/call` - Execute a tool
- `GET /docs` - API documentation

### 3. Tool Registry (`protocol/tools.py`)

Central registry for MCP tool management.

**Responsibilities**:
- Tool registration/discovery
- Input validation
- Execution orchestration
- Performance tracking

### 4. SAP Tools (`sap/tools.py`)

Implements MCP tools for SAP operations.

**Available Tools**:
- `sap_authenticate` - Establish SAP session
- `sap_query` - Query OData services
- `sap_list_services` - Discover services

### 5. SAP Client (`sap/client.py`)

Low-level SAP Gateway OData client.

**Features**:
- CSRF token management
- Session pooling
- SSL/TLS configuration
- Retry logic with exponential backoff

## Request Flow

### Stdio MCP Client

```
Client → stdio_server → Tool Registry → SAP Tool → SAP Client → SAP Gateway
```

### HTTP Client

```
HTTP Client → FastAPI → Tool Registry → SAP Tool → SAP Client → SAP Gateway
```

## Implementation Status

✅ **Completed**:
- MCP stdio server with tool registration
- HTTP server with FastAPI
- SAP client with authentication and OData support
- Tool registry with execution tracking
- 3 core tools (authenticate, query, list_services)
- Configuration management

🚧 **In Progress**:
- Additional SAP tools (create_order, get_metadata)
- Comprehensive testing
- Production deployment configurations

📋 **Planned**:
- Caching layer (Redis)
- Advanced monitoring (Prometheus)
- Multi-tenant support
- Additional SAP modules

"""FastAPI MCP Server implementation"""

import time
import uuid
from datetime import datetime
from typing import Any, Optional

import structlog
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from ..config.settings import get_config
from .schemas import (
    HealthResponse,
    ListToolsResponse,
    MCPError,
    MCPRequest,
    MCPResponse,
    ToolCallRequest,
)
from .tools import tool_registry

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class MCPServer:
    """MCP Protocol Server implementation"""

    def __init__(self) -> None:
        self.app = FastAPI(
            title="SAP Gateway MCP Server",
            description="Model Context Protocol server for SAP Gateway integration",
            version="0.1.0",
            docs_url="/docs",
            openapi_url="/openapi.json",
        )
        self.config = get_config()
        self._setup_middleware()
        self._setup_routes()

    def _setup_middleware(self) -> None:
        """Setup FastAPI middleware"""
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # GZip compression
        self.app.add_middleware(GZipMiddleware, minimum_size=500)

        # Request logging middleware
        @self.app.middleware("http")
        async def logging_middleware(request: Request, call_next: Any) -> Any:
            # Generate correlation ID
            correlation_id = str(uuid.uuid4())
            request.state.correlation_id = correlation_id

            start_time = time.perf_counter()

            # Log request
            logger.info(
                "Request started",
                method=request.method,
                url=str(request.url),
                correlation_id=correlation_id,
            )

            # Process request
            response = await call_next(request)

            # Calculate duration
            process_time = time.perf_counter() - start_time

            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Process-Time"] = str(process_time)

            # Log response
            logger.info(
                "Request completed",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                process_time=process_time,
                correlation_id=correlation_id,
            )

            return response

    def _setup_routes(self) -> None:
        """Setup FastAPI routes"""

        @self.app.get("/health", response_model=HealthResponse)
        async def health_check() -> HealthResponse:
            """Health check endpoint"""
            return HealthResponse(
                status="healthy",
                version="0.1.0",
                timestamp=datetime.utcnow().isoformat(),
                dependencies={
                    "sap_gateway": "unknown",  # Will be updated when SAP client is implemented
                    "tool_registry": f"{len(tool_registry.get_tool_names())} tools registered",
                },
            )

        @self.app.get("/health/detailed")
        async def detailed_health_check() -> dict[str, Any]:
            """Detailed health check with tool statistics"""
            tool_stats = tool_registry.get_statistics()
            return {
                "status": "healthy",
                "version": "0.1.0",
                "timestamp": datetime.utcnow().isoformat(),
                "dependencies": {
                    "sap_gateway": "unknown",
                    "tool_registry": f"{len(tool_registry.get_tool_names())} tools registered",
                },
                "tool_statistics": tool_stats,
                "server_info": {
                    "python_version": "3.11+",
                    "fastapi_version": "0.116.1",
                    "config": {
                        "log_level": self.config.server.log_level,
                        "max_workers": self.config.server.max_workers,
                    },
                },
            }

        @self.app.get("/ready")
        async def readiness_check() -> dict[str, Any]:
            """Readiness check for Kubernetes"""
            # Check if essential services are ready
            tool_count = len(tool_registry.get_tool_names())
            if tool_count == 0:
                raise HTTPException(status_code=503, detail="No tools registered")

            return {"status": "ready", "tools_registered": tool_count}

        @self.app.get("/tools", response_model=ListToolsResponse)
        async def list_tools() -> ListToolsResponse:
            """List all available MCP tools"""
            tools = tool_registry.list_tools()
            return ListToolsResponse(tools=tools)

        @self.app.post("/tools/call")
        async def call_tool(request: ToolCallRequest) -> Any:
            """Call an MCP tool"""
            try:
                response = await tool_registry.call_tool(request)
                return response
            except Exception as e:
                logger.error("Tool call failed", error=str(e), tool_name=request.name)
                raise HTTPException(
                    status_code=500, detail=f"Tool execution failed: {str(e)}"
                )

        @self.app.post("/mcp")
        async def mcp_endpoint(request: MCPRequest) -> MCPResponse:
            """Main MCP protocol endpoint"""
            try:
                if request.method == "tools/list":
                    tools = tool_registry.list_tools()
                    return MCPResponse(
                        id=request.id,
                        result={"tools": [tool.dict() for tool in tools]},
                    )

                elif request.method == "tools/call":
                    if not request.params:
                        raise ValueError("Missing parameters for tool call")

                    tool_request = ToolCallRequest(**request.params)
                    result = await tool_registry.call_tool(tool_request)

                    return MCPResponse(id=request.id, result=result.dict())

                else:
                    return MCPResponse(
                        id=request.id,
                        error=MCPError(
                            code=-32601,
                            message=f"Method not found: {request.method}",
                        ),
                    )

            except Exception as e:
                logger.error(
                    "MCP request failed",
                    error=str(e),
                    method=request.method,
                )
                return MCPResponse(
                    id=request.id,
                    error=MCPError(code=-32603, message=f"Internal error: {str(e)}"),
                )

        @self.app.exception_handler(Exception)
        async def global_exception_handler(
            request: Request, exc: Exception
        ) -> JSONResponse:
            """Global exception handler"""
            correlation_id = getattr(request.state, "correlation_id", "unknown")

            logger.error(
                "Unhandled exception",
                error=str(exc),
                correlation_id=correlation_id,
                exc_info=True,
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": 500,
                        "message": "Internal server error",
                        "correlation_id": correlation_id,
                    }
                },
            )


# Create server factory function
def create_server() -> MCPServer:
    """Create a new MCPServer instance"""
    return MCPServer()


def create_app() -> FastAPI:
    """Create FastAPI application"""
    server = create_server()
    return server.app


# Lazy app creation
app: Optional[FastAPI] = None


def get_app() -> FastAPI:
    """Get or create FastAPI application"""
    global app
    if app is None:
        app = create_app()
    return app


# Export for use with uvicorn
__all__ = ["get_app", "MCPServer", "create_server", "create_app"]

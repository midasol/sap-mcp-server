"""Main server entry point for SAP MCP Server"""

import uvicorn

from .config.settings import get_config


def run_server() -> None:
    """Run the MCP server with proper configuration"""
    config = get_config()

    uvicorn.run(
        "sap_mcp.protocol.server:get_app",
        host=config.server.host,
        port=config.server.port,
        log_level=config.server.log_level.lower(),
        workers=config.server.max_workers,
        reload=config.server.reload,
        factory=True,
    )


if __name__ == "__main__":
    run_server()

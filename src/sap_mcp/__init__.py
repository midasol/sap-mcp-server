"""
SAP Gateway MCP Server

A Model Context Protocol (MCP) server for SAP Gateway integration.
Provides standardized tools for interacting with SAP OData services.
"""

__version__ = "0.1.0"
__author__ = "SAP MCP Team"
__email__ = "sap-mcp@company.com"
__license__ = "MIT"

from .config.settings import AppConfig

# from .sap.client import SAPClient  # TODO: Create SAP client module
from .protocol.server import MCPServer

__all__ = [
    "AppConfig",
    # "SAPClient",  # TODO: Uncomment when SAP client is implemented
    "MCPServer",
    "__version__",
]

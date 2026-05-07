"""SAP MCP Tools - Modular tool registration"""

import logging

from .base import MCPTool, ToolRegistry, tool_registry
from .auth_tool import SAPAuthenticateTool
from .query_tool import SAPQueryTool
from .entity_tool import SAPGetEntityTool
from .service_tool import SAPListServicesTool

logger = logging.getLogger(__name__)

__all__ = [
    "MCPTool",
    "ToolRegistry",
    "tool_registry",
    "SAPAuthenticateTool",
    "SAPQueryTool",
    "SAPGetEntityTool",
    "SAPListServicesTool",
    "register_sap_tools",
]


def register_sap_tools() -> None:
    """Register all SAP tools with the global registry"""
    tool_registry.register(SAPAuthenticateTool())
    tool_registry.register(SAPQueryTool())
    tool_registry.register(SAPGetEntityTool())
    tool_registry.register(SAPListServicesTool())
    logger.info("Registered 4 SAP tools")


# Auto-register on import
register_sap_tools()

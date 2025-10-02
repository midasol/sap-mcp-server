"""SAP Gateway MCP Tools"""

import logging
from typing import Any, Dict

from ..config.settings import SAPConnectionConfig
from ..protocol.tools import MCPTool, tool_registry
from .client import SAPClient

logger = logging.getLogger(__name__)


class SAPAuthenticateTool(MCPTool):
    """Tool for authenticating with SAP Gateway"""

    @property
    def name(self) -> str:
        return "sap_authenticate"

    @property
    def description(self) -> str:
        return "Authenticate with SAP Gateway using username and password"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "SAP Gateway host URL"},
                "username": {"type": "string", "description": "SAP username"},
                "password": {"type": "string", "description": "SAP password"},
                "client": {
                    "type": "string",
                    "description": "SAP client number (optional)",
                    "default": "100",
                },
            },
            "required": ["host", "username", "password"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute authentication"""
        try:
            config = SAPConnectionConfig(
                host=params["host"],
                username=params["username"],
                password=params["password"],
                client=params.get("client", "100"),
            )

            async with SAPClient(config) as client:
                success = await client.authenticate()

            if success:
                return {
                    "success": True,
                    "message": "Successfully authenticated with SAP Gateway",
                    "host": params["host"],
                    "client": config.client,
                }
            else:
                return {"success": False, "error": "Authentication failed"}

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {"success": False, "error": str(e)}


class SAPQueryTool(MCPTool):
    """Tool for querying SAP OData services"""

    @property
    def name(self) -> str:
        return "sap_query"

    @property
    def description(self) -> str:
        return "Query SAP OData service entity sets with optional filters"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "service": {"type": "string", "description": "OData service name"},
                "entity_set": {
                    "type": "string",
                    "description": "Entity set name to query",
                },
                "filter": {
                    "type": "string",
                    "description": "OData filter expression (optional)",
                },
                "select": {
                    "type": "string",
                    "description": "Comma-separated list of fields to select (optional)",
                },
                "top": {
                    "type": "integer",
                    "description": "Maximum number of records to return (optional)",
                },
                "skip": {
                    "type": "integer",
                    "description": "Number of records to skip (optional)",
                },
            },
            "required": ["service", "entity_set"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OData query"""
        try:
            # Build query parameters
            query_params = {}
            if "filter" in params:
                query_params["$filter"] = params["filter"]
            if "select" in params:
                query_params["$select"] = params["select"]
            if "top" in params:
                query_params["$top"] = params["top"]
            if "skip" in params:
                query_params["$skip"] = params["skip"]

            # For now, return a mock response
            # TODO: Implement actual SAP Gateway query when client is ready
            return {
                "success": True,
                "service": params["service"],
                "entity_set": params["entity_set"],
                "query_params": query_params,
                "message": "Query would be executed (mock response)",
                "note": "Actual SAP Gateway integration pending",
            }

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {"success": False, "error": str(e)}


class SAPListServicesTool(MCPTool):
    """Tool for listing available SAP OData services"""

    @property
    def name(self) -> str:
        return "sap_list_services"

    @property
    def description(self) -> str:
        return "List all available SAP OData services"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available services"""
        try:
            # Mock response for now
            return {
                "success": True,
                "services": [
                    "Z_SALES_ORDER_GENAI_SRV",
                    "Z_CUSTOMER_SRV",
                    "Z_MATERIAL_SRV",
                ],
                "message": "Mock service list (actual implementation pending)",
            }

        except Exception as e:
            logger.error(f"Failed to list services: {e}")
            return {"success": False, "error": str(e)}


# Register all tools
def register_sap_tools() -> None:
    """Register all SAP tools with the global registry"""
    tool_registry.register(SAPAuthenticateTool())
    tool_registry.register(SAPQueryTool())
    tool_registry.register(SAPListServicesTool())
    logger.info("Registered 3 SAP tools")


# Auto-register on import
register_sap_tools()

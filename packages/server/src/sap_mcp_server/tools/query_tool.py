"""SAP OData Query Tool"""

import logging
from typing import Any, Dict

from sap_mcp_server.config.loader import get_services_config
from sap_mcp_server.config.settings import get_config
from sap_mcp_server.core.sap_client import SAPClient
from sap_mcp_server.tools.base import MCPTool

logger = logging.getLogger(__name__)


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
            # Get SAP connection configuration
            config = get_config(require_sap=True)
            sap_config = config.sap
            services_config = get_services_config()

            # Find service path
            service_info = services_config.get_service(params["service"])
            if not service_info:
                raise ValueError(f"Service '{params['service']}' not found in configuration")
            service_path = service_info.path

            # Build query parameters
            filters = {"$filter": params["filter"]} if "filter" in params else None
            select_fields = params["select"].split(",") if "select" in params else None
            top = params.get("top")
            skip = params.get("skip")

            # Execute query using SAPClient
            async with SAPClient(config=sap_config) as client:
                result = await client.query_entity_set(
                    service_path=service_path,
                    entity_set=params["entity_set"],
                    filters=filters,
                    select_fields=select_fields,
                    top=top,
                    skip=skip,
                )
            return result

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {"success": False, "error": str(e)}

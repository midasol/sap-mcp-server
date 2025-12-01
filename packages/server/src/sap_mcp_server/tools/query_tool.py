"""SAP OData Query Tool"""

import logging
from typing import Any, Dict, List

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
                "format": {
                    "type": "string",
                    "enum": ["json", "json_compact"],
                    "description": "Output format: 'json' returns raw OData response, 'json_compact' removes __metadata and __deferred navigation links for token efficiency (default: json_compact)",
                    "default": "json_compact",
                },
            },
            "required": ["service", "entity_set"],
        }

    def _transform_response(
        self, data: Dict[str, Any], output_format: str
    ) -> Dict[str, Any]:
        """Transform OData response based on requested format.

        Args:
            data: Raw OData response
            output_format: 'json' for raw response, 'json_compact' for cleaned response

        Returns:
            Transformed response with reduced token usage for json_compact format
        """
        if output_format == "json":
            return data

        # json_compact: Remove __metadata and __deferred navigation links
        results = data.get("d", {}).get("results", [])

        if not results:
            # Handle single entity response (no results array)
            if "d" in data and isinstance(data["d"], dict):
                entity = data["d"]
                clean_entity = {}
                for key, value in entity.items():
                    # Skip metadata
                    if key == "__metadata":
                        continue
                    # Skip deferred navigation links
                    if isinstance(value, dict) and "__deferred" in value:
                        continue
                    clean_entity[key] = value
                return {"result": clean_entity}
            return data

        # Process results array
        clean_results: List[Dict[str, Any]] = []
        for item in results:
            clean_item: Dict[str, Any] = {}
            for key, value in item.items():
                # Skip metadata
                if key == "__metadata":
                    continue
                # Skip deferred navigation links
                if isinstance(value, dict) and "__deferred" in value:
                    continue
                # Keep expanded navigation properties (they have actual data)
                clean_item[key] = value
            clean_results.append(clean_item)

        return {"results": clean_results, "count": len(clean_results)}

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
            output_format = params.get("format", "json_compact")

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

            # Transform response based on format
            return self._transform_response(result, output_format)

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {"success": False, "error": str(e)}

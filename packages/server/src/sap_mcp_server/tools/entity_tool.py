"""SAP Entity Retrieval Tool"""

import logging
from typing import Any, Dict

from sap_mcp_server.tools.base import MCPTool
from sap_mcp_server.core.sap_client import SAPClient
from sap_mcp_server.config.loader import get_services_config
from sap_mcp_server.config.settings import get_services_config_path

logger = logging.getLogger(__name__)


class SAPGetEntityTool(MCPTool):
    """Tool for retrieving a single SAP entity by key"""

    @property
    def name(self) -> str:
        return "sap_get_entity"

    @property
    def description(self) -> str:
        return "Retrieve a single entity from SAP OData service by key (e.g., OrderID)"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "service": {"type": "string", "description": "OData service name"},
                "entity_set": {
                    "type": "string",
                    "description": "Entity set name (e.g., zsd004Set)",
                },
                "entity_key": {
                    "type": "string",
                    "description": "Entity key value (e.g., OrderID like '91000092')",
                },
                "select": {
                    "type": "string",
                    "description": "Comma-separated list of fields to select (optional)",
                },
            },
            "required": ["service", "entity_set", "entity_key"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve entity by key"""
        try:
            from sap_mcp_server.config.settings import get_config

            config = get_config(require_sap=True)

            # Load services configuration
            services_config = get_services_config(get_services_config_path())

            # Validate service exists
            service_config = services_config.get_service(params["service"])
            if not service_config:
                available_services = services_config.list_service_ids()
                return {
                    "success": False,
                    "error": f"Service '{params['service']}' not found in configuration. "
                    f"Available services: {', '.join(available_services)}",
                }

            # Validate entity exists in service
            entity_config = service_config.get_entity(params["entity_set"])
            if not entity_config:
                available_entities = [e.name for e in service_config.entities]
                return {
                    "success": False,
                    "error": f"Entity set '{params['entity_set']}' not found in service '{params['service']}'. "
                    f"Available entities: {', '.join(available_entities)}",
                }

            # Use service path from configuration
            service_path = service_config.path

            # Parse select fields if provided
            select_fields = None
            if "select" in params:
                select_fields = [f.strip() for f in params["select"].split(",")]

            async with SAPClient(config.sap) as client:
                # Authenticate first
                auth_success = await client.authenticate()
                if not auth_success:
                    return {"success": False, "error": "Authentication failed"}

                # Get entity by key
                result = await client.get_entity(
                    service_path=service_path,
                    entity_set=params["entity_set"],
                    entity_key=params["entity_key"],
                    select_fields=select_fields,
                )

                return {
                    "success": True,
                    "service": params["service"],
                    "entity_set": params["entity_set"],
                    "entity_key": params["entity_key"],
                    "key_field": entity_config.key_field,
                    "data": result,
                }

        except Exception as e:
            logger.error(f"Failed to get entity: {e}")
            return {"success": False, "error": str(e)}

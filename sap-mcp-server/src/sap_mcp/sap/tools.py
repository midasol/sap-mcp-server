"""SAP Gateway MCP Tools"""

import logging
from typing import Any, Dict

from ..config.services_loader import get_services_config
from ..config.settings import get_services_config_path
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
            "properties": {},
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute authentication"""
        try:
            from ..config.settings import get_config

            config = get_config(require_sap=True)

            async with SAPClient(config.sap) as client:
                success = await client.authenticate()

            if success:
                return {
                    "success": True,
                    "message": "Successfully authenticated with SAP Gateway",
                    "host": config.sap.host,
                    "client": config.sap.client,
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
            from ..config.settings import get_config

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


class SAPListServicesTool(MCPTool):
    """Tool for listing available SAP OData services"""

    @property
    def name(self) -> str:
        return "sap_list_services"

    @property
    def description(self) -> str:
        return "List all available SAP OData services configured in services.yaml"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available services from configuration"""
        try:
            # Load services configuration
            services_config = get_services_config(get_services_config_path())

            # Build service list with details
            services = []
            for service in services_config.services:
                services.append(
                    {
                        "id": service.id,
                        "name": service.name,
                        "path": service.path,
                        "version": service.version,
                        "description": service.description,
                        "entities": [
                            {
                                "name": entity.name,
                                "key_field": entity.key_field,
                                "description": entity.description,
                            }
                            for entity in service.entities
                        ],
                    }
                )

            return {
                "success": True,
                "count": len(services),
                "services": services,
                "source": "services.yaml configuration",
            }

        except Exception as e:
            logger.error(f"Failed to list services: {e}")
            return {"success": False, "error": str(e)}


# Register all tools
def register_sap_tools() -> None:
    """Register all SAP tools with the global registry"""
    tool_registry.register(SAPAuthenticateTool())
    tool_registry.register(SAPQueryTool())
    tool_registry.register(SAPGetEntityTool())
    tool_registry.register(SAPListServicesTool())
    logger.info("Registered 4 SAP tools")


# Auto-register on import
register_sap_tools()

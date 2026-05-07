"""SAP Services Listing Tool"""

import logging
from typing import Any, Dict

from sap_mcp_server.tools.base import MCPTool
from sap_mcp_server.config.loader import get_services_config
from sap_mcp_server.config.settings import get_services_config_path

logger = logging.getLogger(__name__)


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

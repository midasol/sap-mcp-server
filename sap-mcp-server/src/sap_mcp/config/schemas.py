"""Pydantic models for SAP service configuration from YAML"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class EntityConfig(BaseModel):
    """Configuration for an OData entity set"""

    name: str = Field(..., description="Entity set name (e.g., zsd004Set, CustomerSet)")
    key_field: str = Field(..., description="Primary key field name")
    description: Optional[str] = Field(None, description="Entity description")
    navigations: List[str] = Field(
        default_factory=list, description="Navigation property names"
    )
    default_select: Optional[List[str]] = Field(
        None, description="Default fields to select"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Entity name cannot be empty")
        return v.strip()


class ServiceConfig(BaseModel):
    """Configuration for an OData service"""

    id: str = Field(..., description="Service identifier/name")
    name: str = Field(..., description="Human-readable service name")
    path: str = Field(..., description="Service path (e.g., /SAP/Z_SALES_ORDER_SRV)")
    version: str = Field("v2", description="OData version (v2 or v4)")
    entities: List[EntityConfig] = Field(
        default_factory=list, description="Entity sets in this service"
    )
    custom_headers: Dict[str, str] = Field(
        default_factory=dict, description="Custom HTTP headers for this service"
    )
    description: Optional[str] = Field(None, description="Service description")

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        if v not in ["v2", "v4"]:
            raise ValueError("OData version must be v2 or v4")
        return v

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        if not v.startswith("/"):
            raise ValueError("Service path must start with '/'")
        return v

    def get_entity(self, entity_name: str) -> Optional[EntityConfig]:
        """Get entity configuration by name"""
        for entity in self.entities:
            if entity.name == entity_name:
                return entity
        return None


class GatewayConfig(BaseModel):
    """Configuration for SAP Gateway URL patterns"""

    base_url_pattern: str = Field(
        "https://{host}:{port}/sap/opu/odata",
        description="Base URL pattern for OData services",
    )
    metadata_suffix: str = Field("/$metadata", description="Metadata endpoint suffix")
    service_catalog_path: str = Field(
        "/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection",
        description="Path to service catalog",
    )

    @field_validator("base_url_pattern")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        if "{host}" not in v or "{port}" not in v:
            raise ValueError("base_url_pattern must contain {host} and {port} placeholders")
        return v


class ServicesYAMLConfig(BaseModel):
    """Root configuration model for services YAML file"""

    gateway: GatewayConfig = Field(
        default_factory=GatewayConfig, description="Gateway URL configuration"
    )
    services: List[ServiceConfig] = Field(
        default_factory=list, description="List of SAP OData services"
    )

    def get_service(self, service_id: str) -> Optional[ServiceConfig]:
        """Get service configuration by ID"""
        for service in self.services:
            if service.id == service_id:
                return service
        return None

    def list_service_ids(self) -> List[str]:
        """Get list of all service IDs"""
        return [service.id for service in self.services]

    def get_entity(self, service_id: str, entity_name: str) -> Optional[EntityConfig]:
        """Get entity configuration by service ID and entity name"""
        service = self.get_service(service_id)
        if service:
            return service.get_entity(entity_name)
        return None

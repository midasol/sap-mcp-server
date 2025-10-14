"""YAML configuration loader for SAP services"""

import logging
from pathlib import Path
from typing import Optional

import yaml
from pydantic import ValidationError

from .schemas import ServicesYAMLConfig

logger = logging.getLogger(__name__)


class ServiceConfigurationError(Exception):
    """Raised when service configuration is invalid or cannot be loaded"""

    pass


class ServicesConfigLoader:
    """Loader for SAP services configuration from YAML files"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the configuration loader

        Args:
            config_path: Path to services YAML file. If None, uses default location.
        """
        self.config_path = config_path
        self._config: Optional[ServicesYAMLConfig] = None

    def load(self) -> ServicesYAMLConfig:
        """
        Load and validate services configuration from YAML

        Returns:
            ServicesYAMLConfig: Validated configuration object

        Raises:
            ServiceConfigurationError: If configuration cannot be loaded or is invalid
        """
        if self._config is not None:
            return self._config

        # Determine config file path
        if self.config_path is None:
            # Default location: config/services.yaml relative to package
            package_dir = Path(__file__).parent.parent
            self.config_path = package_dir.parent.parent / "config" / "services.yaml"

        if not self.config_path.exists():
            logger.warning(
                f"Services configuration file not found: {self.config_path}. "
                "Using default configuration."
            )
            return self._load_default_config()

        try:
            # Validate path security (prevent directory traversal)
            resolved_path = self.config_path.resolve()
            if not self._is_safe_path(resolved_path):
                raise ServiceConfigurationError(
                    f"Invalid configuration file path: {self.config_path}"
                )

            # Load YAML file
            with open(resolved_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)

            if not yaml_data:
                logger.warning("Empty YAML configuration, using defaults")
                return self._load_default_config()

            # Validate with Pydantic
            self._config = ServicesYAMLConfig(**yaml_data)
            logger.info(
                f"Loaded {len(self._config.services)} services from {self.config_path}"
            )
            return self._config

        except yaml.YAMLError as e:
            raise ServiceConfigurationError(
                f"Failed to parse YAML configuration: {str(e)}"
            )
        except ValidationError as e:
            raise ServiceConfigurationError(
                f"Invalid service configuration: {str(e)}"
            )
        except Exception as e:
            raise ServiceConfigurationError(
                f"Failed to load service configuration: {str(e)}"
            )

    def reload(self) -> ServicesYAMLConfig:
        """Reload configuration from file"""
        self._config = None
        return self.load()

    def _is_safe_path(self, path: Path) -> bool:
        """
        Validate that path is safe (prevent directory traversal attacks)

        Args:
            path: Resolved path to check

        Returns:
            bool: True if path is safe
        """
        try:
            # Check if path is absolute and doesn't contain suspicious patterns
            if not path.is_absolute():
                return False

            # Path should not contain parent directory references in resolved form
            path_str = str(path)
            if ".." in path_str or path_str.startswith("/etc"):
                return False

            return True
        except Exception:
            return False

    def _load_default_config(self) -> ServicesYAMLConfig:
        """
        Load default configuration (fallback when YAML not available)

        Returns:
            ServicesYAMLConfig: Default configuration
        """
        from .schemas import EntityConfig, GatewayConfig, ServiceConfig

        logger.info("Loading default service configuration")

        default_config = ServicesYAMLConfig(
            gateway=GatewayConfig(
                base_url_pattern="https://{host}:{port}/sap/opu/odata",
                metadata_suffix="/$metadata",
                service_catalog_path="/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/ServiceCollection",
            ),
            services=[
                ServiceConfig(
                    id="Z_SALES_ORDER_GENAI_SRV",
                    name="Sales Order GenAI Service",
                    path="/SAP/Z_SALES_ORDER_GENAI_SRV",
                    version="v2",
                    description="Default sales order service for testing",
                    entities=[
                        EntityConfig(
                            name="zsd004Set",
                            key_field="Vbeln",
                            description="Sales orders entity set",
                            default_select=["Vbeln", "Erdat", "Ernam"],
                        )
                    ],
                    custom_headers={},
                )
            ],
        )

        self._config = default_config
        return default_config


# Global loader instance
_loader: Optional[ServicesConfigLoader] = None


def get_services_config(
    config_path: Optional[Path] = None, reload: bool = False
) -> ServicesYAMLConfig:
    """
    Get services configuration (singleton pattern)

    Args:
        config_path: Optional path to configuration file
        reload: Force reload from file

    Returns:
        ServicesYAMLConfig: Services configuration
    """
    global _loader

    if _loader is None or reload:
        _loader = ServicesConfigLoader(config_path)

    return _loader.load()


def reload_services_config() -> ServicesYAMLConfig:
    """Reload services configuration from file"""
    return get_services_config(reload=True)

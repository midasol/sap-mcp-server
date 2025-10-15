"""Pytest configuration for server tests"""

import os
from pathlib import Path
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest

from sap_mcp_server.config.settings import SAPConnectionConfig
from sap_mcp_server.tools.base import ToolRegistry


@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Test configuration fixture"""
    return {
        "sap_host": os.getenv("SAP_HOST", "test-host"),
        "sap_port": int(os.getenv("SAP_PORT", "443")),
        "sap_username": os.getenv("SAP_USERNAME", "test-user"),
        "sap_password": os.getenv("SAP_PASSWORD", "test-password"),
        "sap_client": os.getenv("SAP_CLIENT", "100"),
    }


@pytest.fixture
def project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def sap_config(test_config: Dict[str, Any]) -> SAPConnectionConfig:
    """Create SAP connection configuration for testing"""
    return SAPConnectionConfig(
        host=test_config["sap_host"],
        port=test_config["sap_port"],
        username=test_config["sap_username"],
        password=test_config["sap_password"],
        client=test_config["sap_client"],
        verify_ssl=False,
        timeout=30,
    )


@pytest.fixture
def mock_sap_client():
    """Create a mock SAP client for testing"""
    client = MagicMock()
    client.authenticate = AsyncMock(return_value=True)
    client.query = AsyncMock(return_value={"results": []})
    client.get_entity = AsyncMock(return_value={"OrderID": "12345"})
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    return client


@pytest.fixture
def tool_registry() -> ToolRegistry:
    """Create a fresh tool registry for each test"""
    return ToolRegistry()


@pytest.fixture
def sample_tool_request() -> Dict[str, Any]:
    """Sample tool call request"""
    return {
        "name": "sap_authenticate",
        "arguments": {},
    }


@pytest.fixture
def sample_query_params() -> Dict[str, Any]:
    """Sample OData query parameters"""
    return {
        "service": "Z_ORDER_SRV",
        "entity_set": "OrderSet",
        "filter": "OrderID eq '12345'",
        "select": "OrderID,CustomerName",
        "top": 10,
        "skip": 0,
    }


@pytest.fixture
def mock_services_config():
    """Mock services configuration"""
    return MagicMock(
        services=[
            MagicMock(
                id="Z_ORDER_SRV",
                name="Order Service",
                path="/sap/opu/odata/sap/Z_ORDER_SRV",
                entities=[
                    MagicMock(
                        name="OrderSet",
                        key_field="OrderID",
                        description="Order entities",
                    )
                ],
            )
        ],
        get_service=MagicMock(
            return_value=MagicMock(
                path="/sap/opu/odata/sap/Z_ORDER_SRV",
                get_entity=MagicMock(
                    return_value=MagicMock(
                        name="OrderSet",
                        key_field="OrderID",
                    )
                ),
            )
        ),
    )

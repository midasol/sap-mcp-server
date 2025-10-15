"""Pytest configuration for server tests"""
import pytest
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "sap_host": os.getenv("SAP_HOST", "test-host"),
        "sap_port": int(os.getenv("SAP_PORT", "443")),
        "sap_username": os.getenv("SAP_USERNAME", "test-user"),
        "sap_password": os.getenv("SAP_PASSWORD", "test-password"),
        "sap_client": os.getenv("SAP_CLIENT", "100"),
    }

@pytest.fixture
def project_root():
    """Get project root directory"""
    return Path(__file__).parent.parent.parent

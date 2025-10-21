"""Pytest configuration for client tests"""
import pytest

@pytest.fixture
def server_url():
    """Test server URL (placeholder for future HTTP endpoint)"""
    return "http://localhost:8000"

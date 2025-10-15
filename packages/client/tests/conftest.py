"""Pytest configuration for client tests"""
import pytest

@pytest.fixture
def server_url():
    """Test server URL"""
    return "http://localhost:8000/sse"

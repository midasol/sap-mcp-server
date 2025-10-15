#!/bin/bash
# 새 디렉토리 구조 생성 스크립트

set -e  # Exit on error

echo "🏗️  Creating new directory structure for SAP MCP refactoring..."

# Change to project root
cd "$(dirname "$0")/.."

# Server structure
echo "📦 Creating server package structure..."
mkdir -p packages/server/src/sap_mcp_server/{core,tools,config,transports,utils}
mkdir -p packages/server/tests/{unit,integration}
mkdir -p packages/server/config

# Client structure
echo "📦 Creating client package structure..."
mkdir -p packages/client/src/sap_mcp_client/transports
mkdir -p packages/client/tests/{unit,integration}

# Shared directories
echo "📁 Creating shared directories..."
mkdir -p examples/{basic,chatbot,advanced}
mkdir -p docs/{architecture,guides,api,examples}

# Create __init__.py files for server
echo "📝 Creating __init__.py files for server..."
touch packages/server/src/sap_mcp_server/__init__.py
touch packages/server/src/sap_mcp_server/core/__init__.py
touch packages/server/src/sap_mcp_server/tools/__init__.py
touch packages/server/src/sap_mcp_server/config/__init__.py
touch packages/server/src/sap_mcp_server/transports/__init__.py
touch packages/server/src/sap_mcp_server/utils/__init__.py
touch packages/server/tests/__init__.py
touch packages/server/tests/unit/__init__.py
touch packages/server/tests/integration/__init__.py

# Create __init__.py files for client
echo "📝 Creating __init__.py files for client..."
touch packages/client/src/sap_mcp_client/__init__.py
touch packages/client/src/sap_mcp_client/transports/__init__.py
touch packages/client/tests/__init__.py
touch packages/client/tests/unit/__init__.py
touch packages/client/tests/integration/__init__.py

# Create test configuration files
echo "⚙️  Creating test configuration files..."
cat > packages/server/tests/conftest.py << 'EOF'
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
EOF

cat > packages/client/tests/conftest.py << 'EOF'
"""Pytest configuration for client tests"""
import pytest

@pytest.fixture
def server_url():
    """Test server URL"""
    return "http://localhost:8000/sse"
EOF

echo "✅ Directory structure created successfully!"
echo ""
echo "Next steps:"
echo "1. Run: ./scripts/migrate_code.sh"
echo "2. Review and update imports"
echo "3. Run tests: pytest packages/server/tests/"

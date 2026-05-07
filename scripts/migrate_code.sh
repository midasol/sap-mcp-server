#!/bin/bash
# 코드 마이그레이션 스크립트

set -e  # Exit on error

echo "🚚 Migrating code to new structure..."

# Change to project root
cd "$(dirname "$0")/.."

# 1. Migrate core modules
echo "📦 Migrating core modules..."
cp sap-mcp-server/src/sap_mcp/sap/client.py packages/server/src/sap_mcp_server/core/sap_client.py
cp sap-mcp-server/src/sap_mcp/sap/auth.py packages/server/src/sap_mcp_server/core/auth.py
cp sap-mcp-server/src/sap_mcp/sap/exceptions.py packages/server/src/sap_mcp_server/core/exceptions.py

# 2. Migrate config modules
echo "⚙️  Migrating config modules..."
cp sap-mcp-server/src/sap_mcp/config/settings.py packages/server/src/sap_mcp_server/config/
cp sap-mcp-server/src/sap_mcp/config/schemas.py packages/server/src/sap_mcp_server/config/
cp sap-mcp-server/src/sap_mcp/config/services_loader.py packages/server/src/sap_mcp_server/config/loader.py

# 3. Copy tools.py (will be split later)
echo "🔧 Copying tools module..."
cp sap-mcp-server/src/sap_mcp/sap/tools.py packages/server/src/sap_mcp_server/tools/tools_legacy.py

# 4. Copy config files
echo "📋 Copying configuration files..."
cp -r sap-mcp-server/config/* packages/server/config/

# 5. Migrate examples
echo "📚 Migrating examples..."
cp sap-mcp-client/examples/order_inquiry_chatbot.py examples/chatbot/
cp sap-mcp-client/examples/stdio_client.py examples/basic/
if [ -f sap-mcp-client/examples/README.md ]; then
    cp sap-mcp-client/examples/README.md examples/
fi

# 6. Copy documentation
echo "📖 Copying documentation..."
cp sap-mcp-server/ARCHITECTURE.md docs/architecture/server.md
cp sap-mcp-server/CONFIGURATION_GUIDE.md docs/guides/configuration.md
cp sap-mcp-server/DEPLOYMENT.md docs/guides/deployment.md

echo "✅ Code migration completed!"
echo ""
echo "⚠️  Important: Run update_imports.py to fix import statements"
echo "   python scripts/update_imports.py"

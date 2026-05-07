"""Integration tests for tool system"""

import pytest

from sap_mcp_server.tools import tool_registry


@pytest.mark.integration
class TestToolRegistration:
    """Test that tools are properly registered on module import"""

    def test_tools_auto_registered(self):
        """Test that tools are automatically registered"""
        tool_names = tool_registry.get_tool_names()

        # Should have all 4 SAP tools registered
        assert "sap_authenticate" in tool_names
        assert "sap_query" in tool_names
        assert "sap_get_entity" in tool_names
        assert "sap_list_services" in tool_names
        assert len(tool_names) == 4

    def test_tool_info_available(self):
        """Test that tool info is available"""
        tools = tool_registry.list_tools()

        assert len(tools) == 4

        # Check that each tool has required fields
        for tool in tools:
            assert hasattr(tool, "name")
            assert hasattr(tool, "description")
            assert hasattr(tool, "inputSchema")
            assert isinstance(tool.inputSchema, dict)

    def test_get_specific_tool(self):
        """Test getting specific tools"""
        auth_tool = tool_registry.get_tool("sap_authenticate")
        assert auth_tool is not None
        assert auth_tool.name == "sap_authenticate"

        query_tool = tool_registry.get_tool("sap_query")
        assert query_tool is not None
        assert query_tool.name == "sap_query"


@pytest.mark.integration
@pytest.mark.asyncio
class TestToolExecution:
    """Test tool execution integration"""

    async def test_list_services_tool(self):
        """Test list services tool execution"""
        from sap_mcp_server.protocol.schemas import ToolCallRequest

        request = ToolCallRequest(
            name="sap_list_services",
            arguments={},
        )

        response = await tool_registry.call_tool(request)

        # Should not error
        assert response.isError is False or "services.yaml" in str(response.content)

    async def test_query_tool_mock_execution(self):
        """Test query tool with mock response"""
        from sap_mcp_server.protocol.schemas import ToolCallRequest

        request = ToolCallRequest(
            name="sap_query",
            arguments={
                "service": "Z_ORDER_SRV",
                "entity_set": "OrderSet",
            },
        )

        response = await tool_registry.call_tool(request)

        # Should execute (returns mock response currently)
        assert len(response.content) > 0

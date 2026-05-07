"""Unit tests for tool base classes and registry"""

from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from sap_mcp_server.protocol.schemas import ToolCallRequest
from sap_mcp_server.tools.base import MCPTool, ToolRegistry


class MockTool(MCPTool):
    """Mock tool for testing"""

    def __init__(self, name: str = "mock_tool", should_fail: bool = False):
        self._name = name
        self._should_fail = should_fail

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return "A mock tool for testing"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
            },
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if self._should_fail:
            raise ValueError("Mock tool failure")
        return {"success": True, "params": params}


@pytest.mark.unit
class TestMCPTool:
    """Tests for MCPTool base class"""

    def test_tool_properties(self):
        """Test that tool properties are accessible"""
        tool = MockTool(name="test_tool")

        assert tool.name == "test_tool"
        assert tool.description == "A mock tool for testing"
        assert isinstance(tool.input_schema, dict)

    def test_to_tool_info(self):
        """Test conversion to ToolInfo schema"""
        tool = MockTool()
        tool_info = tool.to_tool_info()

        assert tool_info.name == "mock_tool"
        assert tool_info.description == "A mock tool for testing"
        assert tool_info.inputSchema == tool.input_schema

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful tool execution"""
        tool = MockTool()
        result = await tool.execute({"param1": "value1"})

        assert result["success"] is True
        assert result["params"]["param1"] == "value1"

    @pytest.mark.asyncio
    async def test_execute_failure(self):
        """Test tool execution failure"""
        tool = MockTool(should_fail=True)

        with pytest.raises(ValueError, match="Mock tool failure"):
            await tool.execute({})


@pytest.mark.unit
class TestToolRegistry:
    """Tests for ToolRegistry class"""

    def test_init(self, tool_registry):
        """Test registry initialization"""
        assert len(tool_registry.get_tool_names()) == 0

    def test_register_tool(self, tool_registry):
        """Test tool registration"""
        tool = MockTool(name="test_tool")
        tool_registry.register(tool)

        assert "test_tool" in tool_registry.get_tool_names()
        assert tool_registry.get_tool("test_tool") == tool

    def test_register_duplicate_tool(self, tool_registry):
        """Test registering duplicate tool (should overwrite)"""
        tool1 = MockTool(name="test_tool")
        tool2 = MockTool(name="test_tool")

        tool_registry.register(tool1)
        tool_registry.register(tool2)

        # Should only have one tool with this name
        assert tool_registry.get_tool_names().count("test_tool") == 1
        # Should be the second tool
        assert tool_registry.get_tool("test_tool") == tool2

    def test_unregister_tool(self, tool_registry):
        """Test tool unregistration"""
        tool = MockTool(name="test_tool")
        tool_registry.register(tool)

        result = tool_registry.unregister("test_tool")

        assert result is True
        assert "test_tool" not in tool_registry.get_tool_names()

    def test_unregister_nonexistent_tool(self, tool_registry):
        """Test unregistering nonexistent tool"""
        result = tool_registry.unregister("nonexistent")
        assert result is False

    def test_get_nonexistent_tool(self, tool_registry):
        """Test getting nonexistent tool"""
        tool = tool_registry.get_tool("nonexistent")
        assert tool is None

    def test_list_tools(self, tool_registry):
        """Test listing all tools"""
        tool1 = MockTool(name="tool1")
        tool2 = MockTool(name="tool2")

        tool_registry.register(tool1)
        tool_registry.register(tool2)

        tools = tool_registry.list_tools()

        assert len(tools) == 2
        tool_names = [t.name for t in tools]
        assert "tool1" in tool_names
        assert "tool2" in tool_names

    @pytest.mark.asyncio
    async def test_call_tool_success(self, tool_registry):
        """Test successful tool call"""
        tool = MockTool(name="test_tool")
        tool_registry.register(tool)

        request = ToolCallRequest(
            name="test_tool",
            arguments={"param1": "value1"},
        )

        response = await tool_registry.call_tool(request)

        assert response.isError is False
        assert len(response.content) == 1
        assert "success" in response.content[0]["text"]

    @pytest.mark.asyncio
    async def test_call_nonexistent_tool(self, tool_registry):
        """Test calling nonexistent tool"""
        request = ToolCallRequest(
            name="nonexistent",
            arguments={},
        )

        response = await tool_registry.call_tool(request)

        assert response.isError is True
        assert "not found" in response.content[0]["text"]

    @pytest.mark.asyncio
    async def test_call_tool_failure(self, tool_registry):
        """Test tool call that fails"""
        tool = MockTool(name="failing_tool", should_fail=True)
        tool_registry.register(tool)

        request = ToolCallRequest(
            name="failing_tool",
            arguments={},
        )

        response = await tool_registry.call_tool(request)

        assert response.isError is True
        assert "failed" in response.content[0]["text"].lower()

    @pytest.mark.asyncio
    async def test_execution_statistics(self, tool_registry):
        """Test that execution statistics are tracked"""
        tool = MockTool(name="test_tool")
        tool_registry.register(tool)

        request = ToolCallRequest(name="test_tool", arguments={})

        # Call tool multiple times
        await tool_registry.call_tool(request)
        await tool_registry.call_tool(request)

        stats = tool_registry.get_statistics()

        assert "test_tool" in stats
        assert stats["test_tool"]["call_count"] == 2
        assert stats["test_tool"]["error_count"] == 0
        assert stats["test_tool"]["average_duration"] >= 0

    @pytest.mark.asyncio
    async def test_error_statistics(self, tool_registry):
        """Test that error statistics are tracked"""
        tool = MockTool(name="failing_tool", should_fail=True)
        tool_registry.register(tool)

        request = ToolCallRequest(name="failing_tool", arguments={})

        # Call tool (it will fail)
        await tool_registry.call_tool(request)

        stats = tool_registry.get_statistics()

        assert stats["failing_tool"]["call_count"] == 1
        assert stats["failing_tool"]["error_count"] == 1
        assert stats["failing_tool"]["error_rate"] == 1.0

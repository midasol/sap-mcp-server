"""MCP Tool registry and management"""

import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .schemas import ToolCallRequest, ToolCallResponse, ToolInfo

logger = logging.getLogger(__name__)


class MCPTool(ABC):
    """Base class for all MCP tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name for MCP registration"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON Schema for tool inputs"""
        pass

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        pass

    def to_tool_info(self) -> ToolInfo:
        """Convert to MCP ToolInfo schema"""
        return ToolInfo(
            name=self.name, description=self.description, inputSchema=self.input_schema
        )


class ToolRegistry:
    """Registry for managing MCP tools"""

    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}
        self._execution_stats: Dict[str, Dict[str, Any]] = {}

    def register(self, tool: MCPTool) -> None:
        """Register a tool"""
        if tool.name in self._tools:
            logger.warning(f"Tool '{tool.name}' already registered, overwriting")

        self._tools[tool.name] = tool
        self._execution_stats[tool.name] = {
            "call_count": 0,
            "total_duration": 0.0,
            "error_count": 0,
            "last_called": None,
        }
        logger.info(f"Registered tool: {tool.name}")

    def unregister(self, tool_name: str) -> bool:
        """Unregister a tool"""
        if tool_name in self._tools:
            del self._tools[tool_name]
            del self._execution_stats[tool_name]
            logger.info(f"Unregistered tool: {tool_name}")
            return True
        return False

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> List[ToolInfo]:
        """List all registered tools"""
        return [tool.to_tool_info() for tool in self._tools.values()]

    def get_tool_names(self) -> List[str]:
        """Get list of registered tool names"""
        return list(self._tools.keys())

    async def call_tool(self, request: ToolCallRequest) -> ToolCallResponse:
        """Execute a tool call"""
        tool_name = request.name
        correlation_id = str(uuid.uuid4())

        logger.info(f"Calling tool '{tool_name}' [correlation_id: {correlation_id}]")

        # Check if tool exists
        tool = self.get_tool(tool_name)
        if not tool:
            error_msg = f"Tool '{tool_name}' not found"
            logger.error(f"{error_msg} [correlation_id: {correlation_id}]")
            return ToolCallResponse(
                content=[{"type": "text", "text": error_msg}], isError=True
            )

        # Execute tool with performance tracking
        start_time = time.time()
        try:
            result = await tool.execute(request.arguments)
            duration = time.time() - start_time

            # Update statistics
            stats = self._execution_stats[tool_name]
            stats["call_count"] += 1
            stats["total_duration"] += duration
            stats["last_called"] = time.time()

            logger.info(
                f"Tool '{tool_name}' executed successfully in {duration:.3f}s "
                f"[correlation_id: {correlation_id}]"
            )

            result_text = result if isinstance(result, str) else str(result)
            return ToolCallResponse(
                content=[{"type": "text", "text": result_text}],
                isError=False,
            )

        except Exception as e:
            duration = time.time() - start_time

            # Update error statistics
            stats = self._execution_stats[tool_name]
            stats["error_count"] += 1
            stats["last_called"] = time.time()

            error_msg = f"Tool execution failed: {str(e)}"
            logger.error(
                f"Tool '{tool_name}' failed after {duration:.3f}s: {str(e)} "
                f"[correlation_id: {correlation_id}]"
            )

            return ToolCallResponse(
                content=[{"type": "text", "text": error_msg}], isError=True
            )

    def get_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get execution statistics for all tools"""
        stats = {}
        for tool_name, raw_stats in self._execution_stats.items():
            call_count = raw_stats["call_count"]
            avg_duration = (
                raw_stats["total_duration"] / call_count if call_count > 0 else 0
            )
            error_rate = raw_stats["error_count"] / call_count if call_count > 0 else 0

            stats[tool_name] = {
                "call_count": call_count,
                "error_count": raw_stats["error_count"],
                "error_rate": error_rate,
                "average_duration": avg_duration,
                "last_called": raw_stats["last_called"],
            }

        return stats


# Global tool registry instance
tool_registry = ToolRegistry()

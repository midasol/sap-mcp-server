"""MCP Protocol schema definitions"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class MCPMethodType(str, Enum):
    """MCP method types"""

    CALL_TOOL = "tools/call"
    LIST_TOOLS = "tools/list"
    GET_PROMPT = "prompts/get"
    LIST_PROMPTS = "prompts/list"
    LIST_RESOURCES = "resources/list"
    READ_RESOURCE = "resources/read"
    SUBSCRIBE = "resources/subscribe"
    UNSUBSCRIBE = "resources/unsubscribe"


class MCPRequest(BaseModel):
    """MCP request schema"""

    jsonrpc: str = Field(default="2.0", description="JSON-RPC version")
    id: Union[str, int] = Field(..., description="Request ID")
    method: str = Field(..., description="Method name")
    params: Optional[Dict[str, Any]] = Field(
        default=None, description="Method parameters"
    )


class MCPResponse(BaseModel):
    """MCP response schema"""

    jsonrpc: str = Field(default="2.0", description="JSON-RPC version")
    id: Union[str, int] = Field(..., description="Request ID")
    result: Optional[Any] = Field(default=None, description="Method result")
    error: Optional["MCPError"] = Field(default=None, description="Error details")


class MCPError(BaseModel):
    """MCP error schema"""

    code: int = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error data"
    )


class ToolInfo(BaseModel):
    """Tool information schema"""

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    inputSchema: Dict[str, Any] = Field(..., description="JSON Schema for tool inputs")


class ToolCallRequest(BaseModel):
    """Tool call request schema"""

    name: str = Field(..., description="Tool name to call")
    arguments: Dict[str, Any] = Field(
        default_factory=dict, description="Tool arguments"
    )


class ToolCallResponse(BaseModel):
    """Tool call response schema"""

    content: List[Dict[str, Any]] = Field(..., description="Tool response content")
    isError: bool = Field(
        default=False, description="Whether the call resulted in an error"
    )


class ListToolsResponse(BaseModel):
    """List tools response schema"""

    tools: List[ToolInfo] = Field(..., description="Available tools")


class HealthResponse(BaseModel):
    """Health check response schema"""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    timestamp: str = Field(..., description="Current timestamp")
    dependencies: Dict[str, str] = Field(
        default_factory=dict, description="Dependency status"
    )


# Forward reference resolution
MCPResponse.model_rebuild()

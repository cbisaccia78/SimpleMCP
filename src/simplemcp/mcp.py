from typing import Literal, Any

from fastjson_rpc2 import JsonRpcRequest, JsonRpcResponse, UNSET, UnsetType
from pydantic import Field


class MCPRequest(JsonRpcRequest):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int
    params: dict[str, Any] = None


class MCPResponse(JsonRpcResponse):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int
    result: dict[str, Any] = Field(default=UNSET)


class MCPNotification(MCPRequest):
    id: UnsetType = Field(default=UNSET)

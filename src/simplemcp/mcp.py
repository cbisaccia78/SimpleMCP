from typing import Literal

from fastjson_rpc2 import JsonRpcRequest, JsonRpcResponse, UNSET, UnsetType
from pydantic import Field


class MCPRequest(JsonRpcRequest):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int
    params: dict[str, str] = None


class MCPResponse(JsonRpcResponse):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int
    result: dict[str, str] = Field(default=UNSET)


class MCPNotification(MCPRequest):
    id: UnsetType = Field(default=UNSET)


noti = MCPNotification(method="example.notify", params={"key": "value"})

try:
    noti = MCPNotification(
        method="example.notify", params={"key": "value"}, jsonrpc="1.0"
    )
except Exception as e:
    print(f"Error creating MCPNotification with id: {e}")

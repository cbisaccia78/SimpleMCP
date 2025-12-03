from typing import Literal, Any

from fastjson_rpc2 import JsonRpcRequest, JsonRpcResponse, UNSET, UnsetType
from pydantic import Field

from .helpers import UTF8EncodingMixin


class MCPRequest(JsonRpcRequest, UTF8EncodingMixin):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int
    params: dict[str, Any] = None

    def has_metadata(self) -> bool:
        """Return ``True`` if the request includes a ``_meta`` field in ``params``."""

        return self.params is not None and "_meta" in self.params

    @property
    def metadata(self) -> dict[str, Any] | UnsetType:
        """Return the metadata dictionary from the request, if present."""

        if self.has_metadata():
            return self.params.get("_meta", UNSET)
        return UNSET


class MCPResponse(JsonRpcResponse, UTF8EncodingMixin):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int
    result: dict[str, Any] = Field(default=UNSET)

    def has_metadata(self) -> bool:
        """Return ``True`` if the request includes a ``_meta`` field in ``params``."""

        return type(self.result) is dict and "_meta" in self.result

    @property
    def metadata(self) -> dict[str, Any] | UnsetType:
        """Return the metadata dictionary from the response, if present."""

        if self.has_metadata():
            return self.result.get("_meta", UNSET)
        return UNSET


class MCPNotification(MCPRequest, UTF8EncodingMixin):
    id: UnsetType = Field(default=UNSET)

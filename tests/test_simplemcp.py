import pytest
from pydantic import ValidationError

from simplemcp.mcp import MCPRequest, MCPResponse, MCPNotification
from fastjson_rpc2 import ErrorObject, UNSET


def test_request_enforces_jsonrpc_version():
    with pytest.raises(ValidationError):
        request = MCPRequest(jsonrpc="1.0", method="ping", id=1, params={"foo": "bar"})


def test_response_enforces_jsonrpc_version():
    with pytest.raises(ValidationError):
        response = MCPResponse(jsonrpc="1.0", result={"pong": True}, id=1)


def test_response_not_both_error_and_result():
    with pytest.raises(ValidationError):
        response = MCPResponse(
            result={"pong": True},
            error={"code": -32601, "message": "Method not found"},
            id=1,
        )


def test_notification_enforces_no_id():
    with pytest.raises(ValidationError):
        request = MCPNotification(method="ping", id=1, params={"foo": "bar"})


def test_response_accepts_result_and_flags_non_error():
    response = MCPResponse(result={"pong": True}, id=1)

    assert response.is_error() is False
    assert response.error is UNSET


def test_response_accepts_error_and_flags_error():
    response = MCPResponse(
        error=ErrorObject(code=-32601, message="Method not found"),
        id=1,
    )

    assert response.is_error() is True
    assert response.result is UNSET


def test_response_rejects_both_result_and_error():
    with pytest.raises(ValidationError):
        MCPResponse(
            result="nope",
            error=ErrorObject(code=-32000, message="Custom"),
            id=1,
        )

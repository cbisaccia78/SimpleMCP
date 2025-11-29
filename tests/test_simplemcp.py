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


def test_notification_enforces_jsonrpc_version():
    with pytest.raises(ValidationError):
        notification = MCPNotification(
            jsonrpc="1.0", method="ping", params={"foo": "bar"}
        )


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
        error={"code": -32601, "message": "Method not found"},
        id=1,
    )

    assert response.is_error() is True
    assert response.result is UNSET


def test_response_rejects_both_result_and_error():
    with pytest.raises(ValidationError):
        MCPResponse(
            result={"nope": True},
            error={"code": -32000, "message": "Custom"},
            id=1,
        )


def test_response_metadata():
    response = MCPResponse(
        result={"data": 42, "_meta": {"info": "test"}},
        id=1,
    )

    assert response.has_metadata() is True
    assert response.metadata == {"info": "test"}

    response = MCPResponse(
        result={"data": 42},
        id=1,
    )

    assert response.has_metadata() is False
    assert response.metadata is UNSET


def test_request_metadata():
    request = MCPRequest(
        method="do_something",
        id=1,
        params={"param1": "value1", "_meta": {"info": "test"}},
    )

    assert request.has_metadata() is True

    request = MCPRequest(
        method="do_something",
        id=1,
        params={"param1": "value1"},
    )

    assert request.has_metadata() is False


def test_notification_metadata():
    notification = MCPNotification(
        method="notify_event",
        params={"event": "started", "_meta": {"info": "test"}},
    )

    assert notification.has_metadata() is True

    notification = MCPNotification(
        method="notify_event",
        params={"event": "started"},
    )

    assert notification.has_metadata() is False

from json import loads

from subprocess import Popen, PIPE
from logging import error, debug
from threading import Thread, Lock
from concurrent.futures import Future
from enum import Enum

from .messages import MCPRequest
from .constants import LATEST_PROTOCOL_VERSION
from .helpers import UTF8EncodingMixin


class ClientState(Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"


class PendingRequests:
    def __init__(self):
        self._lock = Lock()
        self._pending: dict[int | str, Future[MCPRequest]] = {}

    def register(self, msg_id, future):
        with self._lock:
            self._pending[msg_id] = future

    def resolve(self, msg_id, result):
        with self._lock:
            future = self._pending.pop(msg_id, None)
        if future:
            future.set_result(result)


class Client:
    def __init__(self, server_command: str, server_args: list[str]) -> None:
        self.server_command = server_command
        self.server_args = server_args

        self.state: ClientState = ClientState.UNINITIALIZED

        self.pending_requests = PendingRequests()

        self.server_process = Popen(
            [self.server_command] + self.server_args,
            text=False,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            bufsize=0,
        )

        self.server_reader_thread = Thread(target=self.server_stdio_reader, daemon=True)
        self.server_reader_thread.start()

        # Initialization message
        init_message = MCPRequest(
            method="initialize",
            params={
                "protocolVersion": LATEST_PROTOCOL_VERSION,
            },
            id=1,
        )

        response_future = self.send_mcp_message(init_message.id, init_message)

        self.state = ClientState.INITIALIZING

        response = response_future.result(timeout=10)

        self.state = ClientState.READY

    def server_stdio_reader(self):
        if self.server_process.stdout is None:
            error("Server process stdout is not available.")
            return

        for line in self.server_process.stdout:
            try:
                msg = loads(line.decode("utf-8"))
                debug(f"Received server message: {msg}")
            except Exception as e:
                error(f"Failed to decode server message: {e}")

    def send_mcp_message(
        self, message_id: int, message: UTF8EncodingMixin
    ) -> Future[MCPRequest]:
        if self.server_process.stdin:
            debug(f"Sending message to server: {message}")
            self.server_process.stdin.write(message.encode_utf8())
            self.server_process.stdin.flush()
            response_future = Future()
            self.pending_requests.register(message_id, response_future)
            return response_future

        else:
            error("Server process stdin is not available.")

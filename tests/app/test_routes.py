import pytest
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient

from cado.app.app import app as cado_app

API_ENDPOINT = "/stream"


@pytest.fixture(scope="module")
def fast_api() -> FastAPI:
    return cado_app


@pytest.fixture(scope="module")
def test_client(fast_api: FastAPI) -> TestClient:
    return TestClient(fast_api)


class TestRoutes:

    def test_run_cell(self, test_client: TestClient):
        with test_client.websocket_connect(API_ENDPOINT) as socket:
            socket: WebSocket
            socket.send_json({
                "message": "test",
            })
            response_json = socket.receive_json()

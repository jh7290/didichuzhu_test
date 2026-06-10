import json
import socket
import threading
import time
from pathlib import Path

import pytest

from common.config import BASE_URL, VALID_PASSWORD, VALID_PHONE
from common.request_util import RequestUtil
from server.mock_server import MockHandler
from http.server import HTTPServer


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path):
    path = PROJECT_ROOT / relative_path
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_port_open(host="127.0.0.1", port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def mock_server():
    """Auto-start mock server when pytest runs.

    This avoids ConnectionRefusedError when you run tests directly in PyCharm.
    """
    if is_port_open():
        yield
        return

    server = HTTPServer(("127.0.0.1", 8000), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    for _ in range(20):
        if is_port_open():
            break
        time.sleep(0.1)

    yield

    server.shutdown()
    server.server_close()


@pytest.fixture(scope="session")
def api():
    return RequestUtil(BASE_URL)


@pytest.fixture(scope="session")
def login_cases():
    return load_json("data/login_cases.json")


@pytest.fixture(scope="session")
def order_cases():
    return load_json("data/order_cases.json")


@pytest.fixture
def token(api):
    response = api.post("/login", json={
        "phone": VALID_PHONE,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def auth_headers(token):
    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }


@pytest.fixture
def created_order(api, auth_headers):
    body = {
        "start_place": "学校",
        "end_place": "火车站",
        "driver_count": 3,
        "price": 28.5
    }
    response = api.post("/orders", json=body, headers=auth_headers)
    assert response.status_code == 201
    return response.json()

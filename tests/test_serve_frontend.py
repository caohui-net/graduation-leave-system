import importlib.util
import os
import socket
import threading
import urllib.request
from pathlib import Path

import pytest


def load_server_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "serve-frontend.py"
    spec = importlib.util.spec_from_file_location("serve_frontend", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def static_site(tmp_path):
    (tmp_path / "index.html").write_text("ok", encoding="utf-8")
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(original_cwd)


def test_slow_client_does_not_block_other_requests(static_site):
    module = load_server_module()
    server = module.HTTPServer(("127.0.0.1", 0), module.NoCacheHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    slow_socket = socket.create_connection(server.server_address, timeout=1)

    try:
        slow_socket.sendall(b"GET /")

        with urllib.request.urlopen(
            f"http://127.0.0.1:{server.server_address[1]}/",
            timeout=1,
        ) as response:
            assert response.status == 200
            assert response.read() == b"ok"
    except TimeoutError as exc:
        raise AssertionError("slow client blocked another request") from exc
    finally:
        slow_socket.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)

import os
import tempfile

import pytest
from httpx import AsyncClient

from app import main

BASE_URL = "http://test"


def test_startup_event_creates_readyness_file(monkeypatch):
    my_temp_file = tempfile.NamedTemporaryFile(delete=False)
    monkeypatch.setattr(main, "readyness_file_path", my_temp_file.name)
    main.startup_event()
    data = open(my_temp_file.name, "r").read()
    assert data.index("Service is ready") > -1


def test_shutdown_event_deletes_readyness_file(monkeypatch):
    # Do the same as in the previous test. Check that the file exists.
    # Then call shutdown_event and check that the file does not exist.
    my_temp_file = tempfile.NamedTemporaryFile(delete=False)
    monkeypatch.setattr(main, "readyness_file_path", my_temp_file.name)
    main.shutdown_event()
    assert not os.path.exists(my_temp_file.name)


@pytest.mark.parametrize(
    "path, status_code, content",
    [
        ("/", 200, b'{"status":"ok"}'),
        ("/health", 200, b'{"status":"ok"}'),
        ("/fake", 405, b'{"detail":"Method Not Allowed"}'),
    ],
)
async def test_get_methods_in_main(path, status_code, content):
    async with AsyncClient(app=main.app, base_url=BASE_URL) as client:
        response = await client.get(path)
        assert response.status_code == status_code
        assert response.content == content

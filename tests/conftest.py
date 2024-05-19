import pytest
from fastapi.testclient import TestClient

from api import create_server


@pytest.fixture
def client():
    app = create_server()
    return TestClient(app)

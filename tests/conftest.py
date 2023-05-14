import pytest
from fastapi.testclient import TestClient
from api import create_server


@pytest.fixture
def client():
    app = create_server()
    return TestClient(app)


@pytest.fixture
def sample_data():
    return {
        1: ["1"],
        5: ["1", "2", "Fizz", "4", "Buzz"],
        8: ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8"],
        15: [
            "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
            "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"
        ]
    }
from typing import List

import pytest
from fastapi.testclient import TestClient

from api.core.computation import generate_fizzbuzz_sequence


@pytest.mark.api
def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FizzBuzz API!"}


@pytest.mark.api
def test_service_info_endpoint(client: TestClient):
    response = client.get("/service-info")
    assert response.status_code == 200


@pytest.mark.api
def test_health_endpoint(client: TestClient):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.api
def test_compute_endpoint_valid_input(client: TestClient):
    response = client.get("/v0/fizzbuzz?number=15")
    assert response.status_code == 200

    expected_summary = {
        "fizz": 4,
        "buzz": 2,
        "fizzbuzz": 1,
        "digits": 8,
        "sequence": [
            "1",
            "2",
            "Fizz",
            "4",
            "Buzz",
            "Fizz",
            "7",
            "8",
            "Fizz",
            "Buzz",
            "11",
            "Fizz",
            "13",
            "14",
            "FizzBuzz",
        ],
    }
    assert response.json() == expected_summary, "Resulting JSON response did not match"


@pytest.mark.api
def test_compute_endpoint_no_number(client: TestClient):
    response = client.get("/v0/fizzbuzz")
    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.parametrize(
    "value,error",
    [
        (0, "number must a positive integer from 1 to 10^4"),
        (10001, "number must a positive integer from 1 to 10^4"),
        (-1, "number must a positive integer from 1 to 10^4"),
    ],
)
def test_compute_endpoint_invalid_number(client: TestClient, value: int, error: str):
    response = client.get(f"/v0/fizzbuzz?number={value}")
    assert response.status_code == 400
    error_detail = response.json()["message"]
    assert (
        error in error_detail["text"]
    ), f"Expected error message to contain '{error_detail}'"


@pytest.mark.api
@pytest.mark.parametrize(
    "num,expected",
    [
        (1, ["1"]),
        (5, ["1", "2", "Fizz", "4", "Buzz"]),
    ],
)
def test_generate_fizzbuzz_sequence(num: int, expected: List[str]):
    actual = generate_fizzbuzz_sequence(num)
    assert actual == expected, f"Expected {expected}, got {actual}."


@pytest.mark.api
def test_unsupported_routes(client: TestClient):
    response = client.get("/definitely-invalid")
    assert response.status_code == 404, "Endpoint does not exist in API."

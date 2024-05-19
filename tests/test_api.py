from typing import List

import pytest
import requests

from api.computation import generate_fizzbuzz_sequence
from api.models import FizzBuzzSequence


def test_unsupported_routes(client):
    for invalid_endpoint in ("random", "doesnt-exist", "fail"):
        response = client.get(f"/{invalid_endpoint}")
        assert response.status_code == 404, "Endpoint does not exist in API."


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FizzBuzz API!"}


def test_compute_endpoint_valid_input(client):
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


@pytest.mark.parametrize(
    "value,error",
    [
        (0, "number must a positive integer from 1 to 10^4"),
        (10001, "number must a positive integer from 1 to 10^4"),
        (-1, "number must a positive integer from 1 to 10^4"),
    ],
)
def test_compute_endpoint_invalid_number(client, value: int, error: str):
    response = client.get(f"/v0/fizzbuzz?number={value}")
    assert response.status_code == 400
    assert error in response.json()["message"]


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

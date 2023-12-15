import pytest
import requests

from api.computation import generate_fizzbuzz_sequence
from api.models import FizzBuzzSequence, get_data_summary


def test_internet_connectivity():
    url = "https://api.github.com"

    try:
        response = requests.get(url)
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.fail(f"Failed to establish internet connection to {url}")


def test_unsupported_routes(client):
    for invalid_endpoint in ("random", "doesnt-exist", "fail"):
        response = client.get(f"/{invalid_endpoint}")
        assert response.status_code == 404, "Endpoint does not exist in API."


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FizzBuzz API!"}


def test_compute_endpoint_valid_input(client):
    response = client.get("/fizzbuzz?number=15")
    assert response.status_code == 200

    expected_summary = {
        "count": 15,
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
    assert response.json() == expected_summary, ""


def test_compute_endpoint_invalid_input(client):
    # Test numbers outside the allowed range
    invalid_numbers = (0, 10001, -1)
    for invalid in invalid_numbers:
        response = client.get(f"/fizzbuzz?number={invalid}")
        assert (
            "number must a positive integer from 1 to 10^4"
            in response.json()["message"]
        )

    response = client.get("/fizzbuzz?number=abc")
    assert response.status_code == 400


def test_generate_fizzbuzz_sequence(sample_data):
    for number, result in sample_data.items():
        output = generate_fizzbuzz_sequence(number)
        assert output == result, f"Expected {result}, got {output}."


def test_get_data_summary():
    fizzbuzz_sequence = FizzBuzzSequence(["1", "2", "Fizz", "Buzz", "FizzBuzz"])
    expected_summary = {
        "count": 5,
        "fizz": 1,
        "buzz": 1,
        "fizzbuzz": 1,
        "digits": 2,
        "sequence": ["1", "2", "Fizz", "Buzz", "FizzBuzz"],
    }

    summary = get_data_summary(fizzbuzz_sequence)
    assert summary == expected_summary

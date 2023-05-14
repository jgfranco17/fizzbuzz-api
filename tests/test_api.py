import pytest
import requests
from api.models import FizzBuzzSequence, get_data_summary
from api.computation import generate_fizzbuzz_sequence


def test_internet_connectivity():
    url = "https://api.github.com"

    try:
        response = requests.get(url)
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.fail(f"Failed to establish internet connection to {url}")


def test_unsupported_route(client):
    response = client.get("/random")
    assert response.status_code == 404


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
            "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
            "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"
        ]
    }
    assert response.json() == expected_summary, ""


def test_compute_endpoint_invalid_input(client):
    # Test numbers outside the allowed range
    invalid_numbers = (0, 10001, -1)
    for invalid in invalid_numbers:
        response = client.get(f'/fizzbuzz?number={invalid}')
        assert response.json() == {"message": "Invalid input"}, "Expected default error JSON response."

    response = client.get("/fizzbuzz?number=abc")
    expected_error_output = {
        "detail": [{
            "loc": ["query", "number"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }]
    }
    assert response.status_code == 422
    assert response.json() == expected_error_output


def test_generate_fizzbuzz_sequence(sample_data):    
    for number, result in sample_data.items():
        output = generate_fizzbuzz_sequence(number)
        assert output == result, f'Expected {result}, got {output}.'


def test_get_data_summary():
    fizzbuzz_sequence = FizzBuzzSequence(["1", "2", "Fizz", "Buzz", "FizzBuzz"])
    expected_summary = {
        "count": 5,
        "fizz": 1,
        "buzz": 1,
        "fizzbuzz": 1,
        "digits": 2,
        "sequence": ["1", "2", "Fizz", "Buzz", "FizzBuzz"]
    }

    summary = get_data_summary(fizzbuzz_sequence)
    assert summary == expected_summary

import requests

BASE_URL = "https://fizzbuzz-fastapi.onrender.com"


def run_smoke_tests():
    cases = [
        (f"{BASE_URL}/", "message", "Welcome to the FizzBuzz API!"),
        (f"{BASE_URL}/healthz", "status", "healthy"),
        (f"{BASE_URL}/service-info", "project_name", "fizzbuzz-api"),
        (
            f"{BASE_URL}/v0/fizzbuzz?number=5",
            "sequence",
            ["1", "2", "Fizz", "4", "Buzz"],
        ),
    ]
    try:
        for idx, case in enumerate(cases, start=1):
            endpoint, key, value = case
            print(f"[{idx}/{len(cases)}] Testing endpoint: {endpoint}")
            response = requests.get(endpoint)
            assert (
                response.status_code == 200
            ), f"Expected status code 200 but got {response.status_code}"
            assert (
                response.json()[key] == value
            ), f"Endpoint '{endpoint}' response item did not have value '{value}' at '{key}'"

    except AssertionError as e:
        print(f"Endpoint '{endpoint}' failed: {e}")

    else:
        print(f"All {len(cases)} cases passed!")


if __name__ == "__main__":
    run_smoke_tests()

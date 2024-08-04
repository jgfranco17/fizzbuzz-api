import argparse
from http import HTTPStatus
from time import perf_counter_ns
from typing import Optional, Tuple

import requests
from tabulate import tabulate


class SmokeTestRequest:
    """Class-based implementation of a smoke test request."""

    BASE_URL = "https://fizzbuzz-fastapi.onrender.com"

    def __init__(self, endpoint: str, key: str, value: str, http_code: int) -> None:
        # Base attributes
        self.endpoint = endpoint
        self.__url = self.BASE_URL + endpoint
        self.key = key
        self.value = value
        self.http_code = http_code

        # Attributes to be filled after test
        self.__passed = False
        self.__message = None
        self.__duration = 0

    @property
    def passed(self) -> bool:
        return self.__passed

    @property
    def duration(self) -> int:
        return self.__duration

    def run_request(self) -> None:
        request_start_time = perf_counter_ns()
        try:
            response = requests.get(self.__url)
            json_response = response.json()
            assert (
                response.status_code == self.http_code
            ), f"Expected status code {self.http_code} but got {response.status_code}"
            assert (
                json_response[self.key] == self.value
            ), f"Endpoint '{self.endpoint}' response item did not have value '{self.value}' at '{self.key}'"
            self.__passed = True
            self.__message = "No issues found"
        except AssertionError as ae:
            self.__passed = False
            self.__message = f"Results did not match: {ae}"
        except Exception as e:
            self.__passed = False
            self.__message = f"Unexpected error: {e}"
        request_end_time = perf_counter_ns()
        self.__duration = (request_end_time - request_start_time) / (10**6)

    def get_result(self) -> Tuple[str, int, str]:
        test_result = "PASSED" if self.__passed else "FAILED"
        return test_result, self.__duration, self.__message


def run_smoke_tests(output_file: Optional[str] = "") -> None:
    cases = [
        SmokeTestRequest("/", "message", "Welcome to the FizzBuzz API!", HTTPStatus.OK),
        SmokeTestRequest("/healthz", "status", "healthy", HTTPStatus.OK),
        SmokeTestRequest(
            "/service-info", "project_name", "fizzbuzz-api", HTTPStatus.OK
        ),
        SmokeTestRequest(
            "/v0/fizzbuzz?number=5",
            "sequence",
            ["1", "2", "Fizz", "4", "Buzz"],
            HTTPStatus.OK,
        ),
    ]

    # Run test requests
    results_table = []
    for case in cases:
        case.run_request()
        status, duration, message = case.get_result()
        results_table.append(
            [case.endpoint, case.http_code, status, f"{duration:.2f}s", message]
        )

    # Tabulate results
    table_headers = ["Endpoint", "HTTP code", "Result", "Duration (ms)", "Message"]
    summary = (
        tabulate(
            results_table, headers=table_headers, tablefmt="github", numalign="center"
        )
        + "\n"
    )
    print(f"Ran {len(cases)} cases in {sum(case.duration for case in cases):.3f}ms\n")
    print(summary)

    if output_file:
        with open(output_file, "w") as file:
            file.write(summary)
            print(f"Exported results summary: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--export",
        "-e",
        type=str,
        required=False,
        help="Export results data to file",
        default="",
    )
    args = parser.parse_args()
    run_smoke_tests(args.export)

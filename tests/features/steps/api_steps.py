from typing import Dict

from behave import given, then, when  # type: ignore

from tests.features.stubs import TestContext

ENDPOINT_MAP: Dict[str, str] = {
    "index": "/",
    "health-check": "/healthz",
    "service info": "/service-info",
    "metrics": "/metrics",
}


def __parse_keyword(keyword: str):
    keyword = keyword.lower()
    if keyword not in ("fizz", "buzz", "fizzbuzz"):
        raise AssertionError(f"Invalid keyword")
    return keyword


@given("I start the API")
def step_prelaunch_checks(context: TestContext):
    assert context.setup_complete, "Setup was not successful."
    assert context.response is None, "Response was not reset to null."


@given("I send a request to the fizzbuzz endpoint with value {value:d}")
@when("I send a request to the fizzbuzz endpoint with value {value:d}")
def step_get_fizzbuzz_request(context: TestContext, value: int):
    endpoint = f"/v0/fizzbuzz?number={value}"
    context.response = context.mock_server.get(endpoint)


@given("I send a request to the {endpoint_name:S} endpoint")
@when("I send a request to the {endpoint_name:S} endpoint")
def step_get_request(context: TestContext, endpoint_name: str):
    assert endpoint_name in ENDPOINT_MAP.keys(), f"Endpoint '{endpoint_name}' is not recognized."
    endpoint = ENDPOINT_MAP[endpoint_name]
    context.response = context.mock_server.get(endpoint)


@then("the response is returned with status code {status_code:d}")
def step_evaluate_request_status(context: TestContext, status_code: int):
    assert context.response is not None, "Last response was null"
    assert (
        context.response.status_code == status_code
    ), f"Expected status code {status_code} but got {context.response.status_code}"


@then('the response JSON contains "{message:S}" in keys')
def step_evaluate_response_message(context: TestContext, message: str):
    assert context.response is not None, "Last response was null"
    assert message in context.response.json()


@then('the sequence contains {count:d} instances of "{word:S}"')
def step_check_count(context: TestContext, count: int, word: str):
    assert context.response is not None, "Last response was null"
    key = __parse_keyword(word)
    instance_count = context.response.json()[key]
    assert instance_count == count, f"Expected {count} instances of '{word}' but only found {instance_count}"


@then('an error is raised with "{message}" in "{key:S}"')
def step_check_error_output(context: TestContext, message: str, key: str):
    assert context.response is not None, "Last response was null"
    response = context.response.json()["message"][key]
    assert message in response, f"Unexpected error message in '{key}': '{message}' not in {response}"

from behave import given, then, when

from tests.features.stubs import TestContext


def __parse_keyword(keyword: str):
    keyword = keyword.lower()
    if keyword not in ("fizz", "buzz", "fizzbuzz"):
        raise ValueError(f"Invalid keyword")
    return keyword


@given("I start the API")
def step_prelaunch_checks(context: TestContext):
    assert context.setup_complete, "Setup was not successful."
    assert context.response is None, "Response was not reset to None."


@given('I send a request to "{endpoint:S}"')
@when('I send a request to "{endpoint:S}"')
def step_get_request(context: TestContext, endpoint: str):
    context.response = context.mock_server.get(endpoint)


@then("the response is returned with status code {status_code:d}")
def step_evaluate_request_status(context: TestContext, status_code: int):
    assert (
        context.response.status_code == status_code
    ), f"Expected status code {status_code} but got {context.response.status_code}"


@then('the response JSON contains "{message:S}" in keys')
def step_evaluate_response_message(context: TestContext, message: str):
    assert message in context.response.json()


@then('the sequence contains {count:d} instances of "{word:S}"')
def step_check_count(context: TestContext, count: int, word: str):
    key = __parse_keyword(word)
    instance_count = context.response.json()[key]
    assert (
        instance_count == count
    ), f"Expected {count} instances of '{word}' but only found {instance_count}"


@then('an error is raised with "{message}" in "{key:S}"')
def step_check_error_output(context: TestContext, message: str, key: str):
    response = context.response.json()[key]
    assert message in response, f"Unexpected error message in '{key}': {message}"

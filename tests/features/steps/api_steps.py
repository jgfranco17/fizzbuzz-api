from behave import given, then, when
from fastapi import HTTPException


def __parse_keyword(keyword: str):
    keyword = keyword.lower()
    if keyword not in ("fizz", "buzz", "fizzbuzz"):
        raise ValueError(f"Invalid keyword")
    return keyword


@given('I send a request to "{endpoint:S}"')
@when('I send a request to "{endpoint:S}"')
def step_get_request(context, endpoint: str):
    context.response = context.mock_server.get(endpoint)


@then("the response is returned with status code {status_code:d}")
def step_evaluate_request_status(context, status_code: int):
    assert context.response.status_code == status_code


@then('the response JSON contains "{message:S}" in keys')
def step_evaluate_response_message(context, message: str):
    assert message in context.response.json()


@then('the sequence contains {count:d} instances of "{word:S}"')
def step_evaluate_response_message(context, count: int, word: str):
    key = __parse_keyword(word)
    instance_count = context.response.json()[key]
    assert (
        instance_count == count
    ), f"Expected {count} instances of '{word}' but only found {instance_count}"


@then('an error is raised with "{message:S}"')
def step_error_is_raised(context, message: str):
    error_output = context.response.detail
    assert message in error_output, f"Unexpected error: {error_output}"

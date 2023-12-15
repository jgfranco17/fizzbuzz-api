from behave import given, then, when


@given('I send a request to "{endpoint:S}"')
@when('I send a request to "{endpoint:S}"')
def step_get_request(context, endpoint: str):
    context.response = context.mock_server.get(endpoint)


@then("the response is returned with status code {status_code:d}")
def step_evaluate_request_status(context, status_code: int):
    assert context.response.status_code == status_code


@then('the response JSON contains "{message}" in message')
def step_evaluate_response_message(context, message):
    assert message in context.response.json()["message"]

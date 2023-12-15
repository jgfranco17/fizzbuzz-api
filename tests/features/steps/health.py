from behave import given, then, when


@given("I start the test environment")
def step_impl(context):
    context.is_environment_running = True


@when("I run a test")
def step_impl(context):
    context.is_test_started = True


@then("it should pass")
def step_impl(context):
    assert context.is_environment_running
    assert context.is_test_started

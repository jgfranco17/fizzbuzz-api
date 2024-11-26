from behave.runner import Context
from fastapi import Response
from fastapi.testclient import TestClient


class TestContext(Context):
    """Custom Fizzbuzz API context type stub.

    This extends Behave's dynamic Context class to include
    additional attributes used during BDD test execution.

    Primarily used for IDE support for type hints.

    Attributes:
        mock_server (TestClient): Mock API server to run against
        setup_complete (bool): True when the test setup is complete
        teardown_complete (bool): True when the test teardown is complete
        response (Response): Attribute to store call responses
    """

    mock_server: TestClient
    setup_complete: bool
    teardown_complete: bool
    response: Response

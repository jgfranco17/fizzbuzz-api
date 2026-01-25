from behave.model import Scenario
from fastapi.testclient import TestClient

from api.service import app
from tests.features.stubs import TestContext


def before_all(context: TestContext):
    print("Setting up resources for the entire test run...")
    context.mock_server = TestClient(app)
    context.setup_complete = True
    print("Loaded mock server, ready for feature tests!\n")


def after_all(context: TestContext):
    if context.setup_complete:
        print("Tearing down resources for the entire test run...")
        context.teardown_complete = True


def before_scenario(context: TestContext, scenario: Scenario):
    context.response = None

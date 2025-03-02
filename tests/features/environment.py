from fastapi.testclient import TestClient

from api.service import app


def before_all(context):
    print("\nSetting up resources for the entire test run...")
    context.mock_server = TestClient(app)
    context.setup_complete = True
    print("Loaded mock server, ready for feature tests!\n")


def after_all(context):
    if context.setup_complete:
        print("Tearing down resources for the entire test run...")
        # Perform teardown activities here
        context.teardown_complete = True


def before_scenario(context, scenario):
    context.response = None

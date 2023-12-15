from fastapi.testclient import TestClient

from api import create_server


def __create_mock_server():
    app = create_server()
    return TestClient(app)


def before_all(context):
    print("Setting up resources for the entire test run...")
    context.mock_server = __create_mock_server()
    context.setup_complete = True


def after_all(context):
    if context.setup_complete:
        print("Tearing down resources for the entire test run...")
        # Perform teardown activities here
        context.teardown_complete = True

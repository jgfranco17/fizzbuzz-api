"""
CLI interface for API.
"""
from .utils import load_args
from .models.server import create_server


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python3 -m qr-api` and `$ qr-api `.

    This is the program's entry point.
    """
    print("Launching API...")
    app = create_server()
    config = load_args()
    app.run(port=config.port)

"""
CLI interface for API.
"""
from .utils import load_args
from .server import create_server


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python3 -m fizzbuzz-api` and `$ fizzbuzz-api`.

    This is the program's entry point.
    """
    print("Launching API...")
    app = create_server()
    config = load_args()
    app.run(port=config.port)

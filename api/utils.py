import argparse
from types import SimpleNamespace
from typing import Any, List, Union


def load_args() -> argparse.Namespace:
    """Load and parse command line arguments.

    Returns:
        argparse.Namespace: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true", default=True, help="Enable debug mode"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        required=False,
        help="Port to connect to",
        default=5500,
    )
    args = parser.parse_args()
    return args

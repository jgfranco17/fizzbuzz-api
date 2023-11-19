"""
UTILS.PY

Miscellaneous helper functions for CLI tool management.
"""
import argparse


def load_args() -> argparse.Namespace:
    """
    Load and parse command line arguments.

    Returns:
        argparse.Namespace: parsed arguments
    """
    parser = argparse.ArgumentParser()
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

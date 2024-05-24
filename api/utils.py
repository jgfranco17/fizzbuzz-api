"""
UTILS.PY

Miscellaneous helper functions for CLI tool management.
"""
import argparse
import json
import os
from typing import Any, Dict


def load_args() -> argparse.Namespace:
    """
    Load and parse command line arguments.

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


def read_specs(filepath: str) -> Dict[str, Any]:
    full_filepath = os.path.join(os.path.dirname(__file__), filepath)
    with open(full_filepath, "r") as file:
        data = json.load(file)
    data.update()
    return data

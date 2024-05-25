"""
UTILS.PY

Miscellaneous helper functions for CLI tool management.
"""
import argparse
import json
import os
from types import SimpleNamespace
from typing import Any, Dict, List, Union


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


def unmarshal(
    json_data: Union[dict, List[Any]]
) -> Union[SimpleNamespace, List[SimpleNamespace]]:
    """
    Recursively convert a dictionary to a namespace.
    """
    if isinstance(json_data, dict):
        return SimpleNamespace(
            **{key: unmarshal(value) for key, value in json_data.items()}
        )
    elif isinstance(json_data, list):
        return [unmarshal(item) for item in json_data]
    else:
        return json_data


def marshal(namespace: Union[dict, List[Any]]) -> Union[dict, List[Any]]:
    """
    Recursively convert a namespace to a dictionary.
    """
    if isinstance(namespace, SimpleNamespace):
        return {key: marshal(value) for key, value in vars(namespace).items()}
    elif isinstance(namespace, list):
        return [marshal(item) for item in namespace]
    else:
        return namespace

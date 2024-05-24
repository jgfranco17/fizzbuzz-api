"""
CLI interface for API.
"""
import io
import json
import os

import uvicorn

from .server import create_server
from .utils import load_args


def main():
    """
    The main function executes on commands:
    `python3 -m fizzbuzz-api` and `$ fizzbuzz-api`.

    This is the program's entry point.
    """
    header = r"""
___________.__               __________                          _____ __________.___
\_   _____/|__|______________\______   \____________________   /  _  \\______   \   |
|    __)  |  \___   /\___   /|    |  _/  |  \___   /\___   /  /  /_\  \|     ___/   |
|     \   |  |/    /  /    / |    |   \  |  //    /  /    /  /    |    \    |   |   |
\___  /   |__/_____ \/_____ \|______  /____//_____ \/_____ \ \____|__  /____|   |___|
    \/             \/      \/       \/            \/      \/         \/
    """
    app = create_server()
    config = load_args()
    host = "0.0.0.0" if config.debug else "127.0.0.1"
    print(f"Running FizzBuzz API")
    print(f"Debug mode: {config.debug}")
    print(header)
    uvicorn.run(app, host=host, port=config.port)

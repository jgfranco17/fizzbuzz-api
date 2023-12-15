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

    def get_json_key(*paths, **kwargs):
        """
        Read the contents of a JSON key safely.
        """
        filepath = os.path.join(os.path.dirname(__file__), *paths)
        with open(filepath, "r") as file:
            data = dict(json.load(file))
        key = kwargs.get("key", "version")
        return data.get(key, "none")

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
    version = get_json_key("specs.json", key="version")
    print(f"Running FizzBuzz API v{version}")
    print(header)
    uvicorn.run(app, host="0.0.0.0", port=config.port)

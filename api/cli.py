"""
CLI interface for API.
"""
import io
import os
import uvicorn
from .utils import load_args
from .server import create_server


def main():
    """
    The main function executes on commands:
    `python3 -m fizzbuzz-api` and `$ fizzbuzz-api`.

    This is the program's entry point.
    """
    def read(*paths, **kwargs):
        """
        Read the contents of a text file safely.
        """
        content = ""
        with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
        ) as file:
            content = file.read().strip()
        return content

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
    version = read("VERSION")
    print(f'Running FizzBuzz API v{version}')
    print(header)
    uvicorn.run(app, host="0.0.0.0", port=config.port)

"""
CLI interface for API.
"""
import uvicorn
from .utils import load_args
from .server import create_server


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python3 -m fizzbuzz-api` and `$ fizzbuzz-api`.

    This is the program's entry point.
    """
    header = r"""
___________.__               __________                          _____ __________.___ 
\_   _____/|__|______________\______   \__ __________________   /  _  \\______   \   |
|    __)  |  \___   /\___   /|    |  _/  |  \___   /\___   /  /  /_\  \|     ___/   |
|     \   |  |/    /  /    / |    |   \  |  //    /  /    /  /    |    \    |   |   |
\___  /   |__/_____ \/_____ \|______  /____//_____ \/_____ \ \____|__  /____|   |___|
    \/             \/      \/       \/            \/      \/         \/              
    """
    app = create_server()
    config = load_args()
    print(header)
    uvicorn.run(app, host="0.0.0.0", port=config.port)

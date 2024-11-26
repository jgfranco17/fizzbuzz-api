import argparse
import logging
import subprocess
from pathlib import Path

LOGLEVEL = "INFO"


def __set_logging_level(level: str) -> None:
    """Set the logging level.

    Args:
        level (str): Level of logging for package
    """
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logging.basicConfig(
        level=levels.get(level, logging.INFO),
        format="[%(asctime)s | %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d | %H:%M:%S",
    )
    logging.info(f"Set logging level to {level}")


def run_behave(features_path):
    """
    Run Behave tests.
    """
    behave_command = [
        "behave",
        str(Path(features_path).resolve()),
    ]

    try:
        subprocess.run(behave_command, check=True)
    except subprocess.CalledProcessError as err:
        logging.error(f"Behave execution failed with return code {err.returncode}")


def get_parsed_args():
    parser = argparse.ArgumentParser(description="Customize and run Behave tests.")
    parser.add_argument("features", type=str, help="Path to the features directory.")
    return parser.parse_args()


if __name__ == "__main__":
    __set_logging_level(LOGLEVEL)
    args = get_parsed_args()
    run_behave(args.features)

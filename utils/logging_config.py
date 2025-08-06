import logging
from pathlib import Path
from typing import Optional


VERBOSE_FORMAT = "[%(asctime)s] - [%(levelname)-10s] - %(name)s: %(message)s"
STANDARD_FORMAT = "%(levelname)-10s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

ROOT_DIR = Path(__file__).resolve().parents[1]
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOGGING_PATH = LOGS_DIR / "app.log"


def setup_logging(path: Optional[Path] = None) -> None:
    if path is None:
        path = LOGGING_PATH

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(STANDARD_FORMAT))
    logging.getLogger().addHandler(console_handler)

    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(VERBOSE_FORMAT, datefmt=DATE_FORMAT))
    logging.getLogger().addHandler(file_handler)

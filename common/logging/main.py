import json
import logging
import logging.config
from pathlib import Path
from typing import Any

BASE_PATH = Path(__file__).parent / 'config.json'


def get_logging_config(filepath: Path = BASE_PATH) -> dict[str, Any]:
    with open(filepath, 'r') as f:
        result: dict[str, Any] = json.load(f)
    assert isinstance(result, dict), 'Config must be in key-values format'
    return result


def setup_logging() -> None:
    logging.config.dictConfig(get_logging_config())

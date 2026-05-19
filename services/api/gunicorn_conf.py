import multiprocessing
from pathlib import Path

from common.logging.main import get_logging_config

bind = '0.0.0.0:8000'
workers = max(multiprocessing.cpu_count() * 2, 1)
worker_class = 'uvicorn.workers.UvicornWorker'
logconfig_dict = get_logging_config(
    Path(__file__).parent.parent.parent / 'common/logging/config.prod.json'
)

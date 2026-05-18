import multiprocessing
from pathlib import Path

from common.logging.main import get_logging_config

bind = 'unix:/opt/duo/app.sock'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'
logconfig_dict = get_logging_config(Path('/app/common/logging/config.json'))

from pathlib import Path

import uvicorn

from common.logging.main import get_logging_config

if __name__ == '__main__':
    loggin_config_path = Path('./common/logging/config.json')
    uvicorn.run(
        'services.api.main:app',
        reload=True,
        log_config=get_logging_config(loggin_config_path),
        port=8000,
        host='0.0.0.0',
    )

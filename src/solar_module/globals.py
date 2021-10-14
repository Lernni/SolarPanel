import os

from pathlib import Path

DEBUG = bool(os.environ.get('DEBUG'))

if DEBUG:
    DB_PATH = Path("./cache/db")
    CONFIG_DIR_PATH = Path("./cache/config")
    CONFIG_TEMPLATE_PATH = Path("./config/config.template.ini")
    LOGS_PATH = Path("./cache/logs")
else:
    DB_PATH = Path("/data/db")
    CONFIG_DIR_PATH = Path("/data/config")
    CONFIG_TEMPLATE_PATH = Path("/app/config/config.template.ini")
    LOGS_PATH = Path("/data/logs")
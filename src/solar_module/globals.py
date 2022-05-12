import os
import math

from pathlib import Path

DEBUG = bool(os.environ.get('DEBUG'))

# *** Recording Variables ***

RESOLUTION_DEPTH = 18
MAX_RECORD_COUNT = math.pow(2, RESOLUTION_DEPTH)
# RESOLUTION_DEPTH determines how many resolution layers are created
# e.g. RESOLUTION_DEPTH = 5 -> 2, 4, 8, 16, 32

MAX_RECORDS_PER_PARTITION = 60 * 60 * 24
# Maximum number of records per partition

MAX_CACHE_SIZE = 512
# Maximum number of records with resolution 1 in the cache
# Should be a multiple of 2, to reduce the number of read operations after clearing the cache
# After MAX_CACHE_SIZE records are in the cache, MAX_CACHE_SIZE / 2 records get saved


# *** Evaluation Variables ***

LOW_BATTERY_THRESHOLD = 20
# Battery charging level in percent, below which the red LED is turned on, marking the battery level as low

CORRECTION_INTERVAL = 256
# Time in seconds between correction attempts

MIN_VOLTAGE_AVG = 13.5
# Minimum voltage average, above which capacity correction can be applied

MAX_VOLTAGE_STD = 0.1
# Maximum voltage standard deviation, below which capacity correction can be applied

MAX_CURRENT_STD = 0.5
# Maximum current standard deviation, below which capacity correction can be applied

MAX_CURRENT_DIFF = 0.1
# Maximum current difference, that is allowed between the input and output current


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
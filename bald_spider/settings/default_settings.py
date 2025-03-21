"""
default config
"""
VERSION = 1.0

CONCURRENCY = 16

LOG_LEVEL = "INFO"

VERIFY_SSL = True

REQUEST_TIMEOUT = 60

USE_SESSION = True

DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"

INTERVAL = 60

STATS_DUMP = True

# download_delay
DOWNLOAD_DELAY = 0
RANDOMNESS = True
RANDOM_RANGE = (0.75, 1.25)

# retry
RETRY_HTTP_CODES = [408, 429, 500, 502, 503, 504, 522, 524]
IGNORE_HTTP_CODES = [403, 404]
MAX_RETRY_TIMES = 2
ALLOWED_CODES = []
RETRY_PRIORITY = 1

# filter
FILTER_DEBUG = True
FILTER_CLS = "bald_spider.duplicate_filter.memory_filter.MemoryFilter"

# redis_filter
REDIS_URL = "redis://localhost/0"  # redis://[[username]:[password]]@host:port/db
DECODE_RESPONSES = True
REDIS_KEY = "request_fingerprint"
SAVE_FP = False

DEPTH_PRIORITY = 1
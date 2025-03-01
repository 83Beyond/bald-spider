"""
default config
"""

CONCURRENCY = 16

LOG_LEVEL = "INFO"

VERIFY_SSL = True

REQUEST_TIMEOUT = 60

USE_SESSION = True

DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"
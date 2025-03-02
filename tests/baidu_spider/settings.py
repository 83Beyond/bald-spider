PROJECT_NAME = "baidu_spider"

CONCURRENCY = 4

LOG_LEVEL = "DEBUG"

HEADERS = {}

MIDDLEWARES = [
    # engine side
    "bald_spider.middleware.request_ignore.RequestIgnore",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.default_header.DefaultHeader",
    "baidu_spider.middleware.TestMiddleware",
    "baidu_spider.middleware.TestMiddleware2",
    # downloader side
]

DOWNLOAD_DELAY = 2

USER_AGENT = ""
DEFAULT_HEADERS = {
    "User-Agent": ""
}
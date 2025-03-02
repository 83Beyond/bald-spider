PROJECT_NAME = "baidu_spider"

CONCURRENCY = 4

LOG_LEVEL = "DEBUG"

HEADERS = {}

MIDDLEWARES = [
    # engine side

    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.default_header.DefaultHeader",
    "bald_spider.middleware.response_filter.ResponseFilter",
    "bald_spider.middleware.retry.Retry",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    "bald_spider.middleware.request_ignore.RequestIgnore",

    # "baidu_spider.middleware.TestMiddleware",
    # "baidu_spider.middleware.TestMiddleware2",
    # downloader side
]

EXTENSIONS = [
    "bald_spider.extension.log_interval.LogInterval",
    "bald_spider.extension.log_stats.LogStats",
]

PIPELINES = [
    # "baidu_spider.pipeline.TestPipeline",
    # "bald_spider.pipeline.debug_pipeline.DebugPipeline",
]

DOWNLOAD_DELAY = 2

USER_AGENT = ""
DEFAULT_HEADERS = {
    "User-Agent": ""
}

ALLOWED_CODES = [404]

DB_NAME = "bald_spider"
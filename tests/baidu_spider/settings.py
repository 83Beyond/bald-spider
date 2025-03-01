PROJECT_NAME = "baidu_spider"

CONCURRENCY = 1

LOG_LEVEL = "DEBUG"

HEADERS = {}

MIDDLEWARES = [
    "baidu_spider.middleware.TestMiddleware",
    "baidu_spider.middleware.TestMiddleware2",
]
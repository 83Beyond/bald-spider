PROJECT_NAME = "baidu_spider"

CONCURRENCY = 8

LOG_LEVEL = "INFO"

HEADERS = {}

MIDDLEWARES = [
    # engine side

    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.default_header.DefaultHeader",
    "bald_spider.middleware.response_filter.ResponseFilter",
    "bald_spider.middleware.retry.Retry",
    "baidu_spider.middleware.ProxyMiddleware",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    "bald_spider.middleware.request_ignore.RequestIgnore",

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
    "baidu_spider.pipeline.LayPipeline",
]

DOWNLOAD_DELAY = 1

USER_AGENT = ""
DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

ALLOWED_CODES = [404]

DB_NAME = "bald_spider"

# filter
FILTER_DEBUG = True
# FILTER_CLS = "bald_spider.duplicate_filter.aioredis_filter.AioRedisFilter"
FILTER_CLS = "bald_spider.duplicate_filter.memory_filter.MemoryFilter"
# FILTER_CLS = "bald_spider.duplicate_filter.aioredis_filter.AioRedisFilter"

# redis_filter
# REDIS_URL = "redis://localhost/0"  # redis://[[username]:[password]]@host:port/db
# DECODE_RESPONSES = True
# REDIS_KEY = "request_fingerprint"
# SAVE_FP = False
# REQUEST_DIR = "."  # 没有 REQUEST_DIR 就是基于内存的过滤器，不写文件
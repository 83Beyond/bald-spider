"""
重试中间件.
1. 状态码不对，需要重新请求
408, 429, 500, 502, 503, 504, 522, 524
2. 哪些状态码不需要重新请求
200-300, 403, 404
3. 请求期间报错，需要收集这些错误，当捕获到这些异常的时候，需要重新请求
"""
from typing import List
from asyncio.exceptions import TimeoutError

from aiohttp import ClientConnectionError, ClientTimeout, ClientConnectorSSLError, ClientResponseError
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError
from httpx import RemoteProtocolError, ConnectError, ReadTimeout
from anyio import EndOfStream
from httpcore import ReadError

from bald_spider.stats_collector import StatsCollector
from bald_spider.utils.log import get_logger

_retry_exceptions = [
    ClientConnectionError,
    ClientTimeout,
    ClientConnectorSSLError,
    ClientResponseError,
    RemoteProtocolError,
    ReadError,
    EndOfStream,
    ConnectError,
    TimeoutError,
    ClientPayloadError,
    ReadTimeout,
    ClientConnectorError
]

class Retry:

    def __init__(
            self,
            *,
            retry_http_codes: List,
            ignore_http_codes: List,
            max_retry_times: int,
            retry_exceptions: List,
            stats: StatsCollector
    ):
        self.retry_http_codes = retry_http_codes
        self.ignore_http_codes = ignore_http_codes
        self.max_retry_times = max_retry_times
        self.retry_exceptions = tuple(retry_exceptions + _retry_exceptions)
        self.stats = stats
        self.logger = get_logger(self.__class__.__name__)

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            retry_http_codes=crawler.settings.getlist("RETRY_HTTP_CODES"),
            ignore_http_codes=crawler.settings.getlist("IGNORE_HTTP_CODES"),
            max_retry_times=crawler.settings.getint("MAX_RETRY_TIMES"),
            retry_exceptions=crawler.settings.getlist("RETRY_EXCEPTIONS"),
            stats=crawler.stats
        )
        return o

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.ignore_http_codes:
            return response
        if response.status in self.retry_http_codes:
            # 重试的逻辑
            reason = f"response code: {response.status}"
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exc, spider):
        if (
                isinstance(exc, self.retry_exceptions)
                and not request.meta.get("dont_retry", False)
        ):
            return self._retry(request, type(exc).__name__, spider)

    def _retry(self, request, reason, spider):
        # todo 去重的逻辑还没写，要保证重试的请求不被请求过滤器过滤掉
        # todo 重新发起的请求，优先级应该怎么定
        retry_times = request.meta.get("retry_times", 0)
        if retry_times < self.max_retry_times:
            retry_times += 1
            self.logger.info(f"{spider} {request} {reason} retrying {retry_times} time...")
            request.meta["retry_times"] = retry_times
            self.stats.inc_value("retry_count")
            return request
        else:
            self.logger.warning(
                f"{spider} {request} {reason} retry max {self.max_retry_times} times, give up."
            )
            return None
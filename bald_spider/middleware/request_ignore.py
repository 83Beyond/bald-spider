from bald_spider.event import ignore_request
from bald_spider.utils.log import get_logger
from bald_spider.exceptions import IgnoreRequest


class RequestIgnore:

    def __init__(self, stats, log_level):
        self.logger = get_logger(self.__class__.__name__, log_level)
        self.stats = stats

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            stats=crawler.stats,
            log_level=crawler.settings.get("LOG_LEVEL")
        )
        crawler.subscriber.subscribe(o.request_ignore, event=ignore_request)
        return o

    async def request_ignore(self, exc, request, _spider):
        self.logger.info(f"{request} ignored.")
        self.stats.inc_value(f"request_ignore_count")
        reason = exc.msg
        if reason:
            self.stats.inc_value(f"request_ignore_count/{reason}")

    @staticmethod
    def process_exception(_request, exc, _spider):
        if isinstance(exc, IgnoreRequest):
            return True

from typing import Optional, Callable

from bald_spider import Request
from bald_spider.utils.log import get_logger
from bald_spider.utils.pqueue import SpiderPriorityQueue
from bald_spider.utils.project import load_class, common_call
from bald_spider.utils.request import set_request


class Scheduler:

    def __init__(self, crawler, dupe_filter, stats, log_level, priority):
        self.crawler = crawler
        self.request_queue: Optional[SpiderPriorityQueue] = None
        self.logger = get_logger(self.__class__.__name__, log_level=log_level)
        self.stats = stats
        self.dupe_filter = dupe_filter
        self.priority = priority

    @classmethod
    def create_instance(cls, crawler):
        filter_cls = load_class(crawler.settings.get("FILTER_CLS"))
        o = cls(
            crawler=crawler,
            dupe_filter=filter_cls.create_instance(crawler),
            stats=crawler.stats,
            log_level=crawler.settings.get("LOG_LEVEL"),
            priority=crawler.settings.getint("DEPTH_PRIORITY")
        )
        return o

    def open(self):
        self.request_queue = SpiderPriorityQueue()
        self.logger.info(f"request filter: {self.dupe_filter}")

    async def next_request(self) -> Optional[Request]:
        request = await self.request_queue.get()
        return request

    async def enqueue_request(self, request):
        if (
            not request.dont_filter and
            await common_call(self.dupe_filter.requested, request)
        ):
            self.dupe_filter.log_stats(request)
            return False
        set_request(request, self.priority)
        await self.request_queue.put(request)
        return True

    def idle(self) -> bool:
        return len(self) == 0

    def __len__(self):
        return self.request_queue.qsize()

    async def closed(self):
        if isinstance(closed := getattr(self.dupe_filter, "closed", None), Callable):
            await closed()

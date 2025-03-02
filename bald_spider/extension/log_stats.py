from bald_spider import event
from bald_spider.utils.date import now, date_delta


class LogStats:

    def __init__(self, stats):
        self._stats = stats

    @classmethod
    def create_instance(cls, crawler):
        o = cls(crawler.stats)
        crawler.subscriber.subscribe(o.spider_opened, event=event.spider_opened)
        crawler.subscriber.subscribe(o.spider_closed, event=event.spider_closed)
        crawler.subscriber.subscribe(o.request_scheduled, event=event.request_scheduled)
        crawler.subscriber.subscribe(o.response_received, event=event.response_received)
        return o

    async def spider_opened(self):
        self._stats["start_time"] = now()

    async def spider_closed(self):
        self._stats["end_time"] = now()
        self._stats["cost_time(s)"] = date_delta(self._stats["start_time"], self._stats["end_time"])

    async def request_scheduled(self, _request, _spider):
        self._stats.inc_value("request_scheduled_count")

    async def response_received(self, _response, _spider):
        self._stats.inc_value("response_received_count")
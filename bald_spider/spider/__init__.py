from bald_spider import Request


class Spider:

    def __init__(self):
        if not hasattr(self, "start_urls"):
            self.start_urls = []

    @classmethod
    def create_instance(cls, crawler):
        o = cls()
        o.crawler = crawler
        return o

    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield Request(url=url, dont_filter=True)
        else:  # 兼容 spider 中只有 start_url 的情况
            if hasattr(self, "start_url") and isinstance(getattr(self, "start_url"), str):
                yield Request(getattr(self, "start_url"), dont_filter=True)

    def parse(self, response):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

    async def spider_opened(self):
        pass

    async def spider_closed(self):
        pass

import asyncio
from typing import Optional, Generator, Callable
from inspect import iscoroutine

from bald_spider.core.downloader import Downloader
from bald_spider.core.scheduler import Scheduler
from bald_spider.spider import Spider
from bald_spider.utils.spider import transform


class Engine:

    def __init__(self):
        self.downloader: Optional[Downloader] = None
        self.scheduler: Optional[Scheduler] = None
        self.spider: Optional[Spider] = None
        self.start_requests: Optional[Generator] = None  # Optional 可以是 None

    async def start_spider(self, spider):
        self.spider = spider
        self.downloader = Downloader()
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.start_requests = iter(spider.start_requests())
        await self._open_spider()

    async def _open_spider(self):
        crawling = asyncio.create_task(self.crawl())
        # 这里可以做其他的事情
        await crawling

    async def crawl(self):
        """主逻辑"""
        while True:
            if (request := await self._get_next_request()) is not None:
                # 请求
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)  # noqa

                except StopIteration:
                    self.start_requests = None
                except Exception as exc:
                    break
                else:
                    # 入队
                    await self.enqueue_request(start_request)

    async def _crawl(self, request):
        # todo 实现并发
        outputs = await self._fetch(request)
        # 处理 outputs
        if outputs:
            async for output in outputs:
                print(output)

    async def _fetch(self, request):
        async def _success(response):
            callback: Callable = request.callback or self.spider.parse  # 自定义爬虫脚本的 parse 方法
            if _outputs := callback(response):  # 对 parse 做兼容
                if iscoroutine(_outputs):
                    await _outputs
                else:
                    return transform(_outputs)

        _response = await self.downloader.fetch(request)
        outputs = await _success(_response)  # 生成器，能获取到的前提是 fetch 是成功的
        return outputs

    async def enqueue_request(self, request):
        await self._schedule_request(request)

    async def _schedule_request(self, request):
        # todo 去重
        await self.scheduler.enqueue_request(request)

    async def _get_next_request(self):
        return await self.scheduler.next_request()


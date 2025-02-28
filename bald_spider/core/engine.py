import asyncio
from typing import Optional, Generator, Callable
from inspect import iscoroutine

from bald_spider import Request, Item
from bald_spider.core.downloader import Downloader
from bald_spider.core.scheduler import Scheduler
from bald_spider.exceptions import OutputError
from bald_spider.spider import Spider
from bald_spider.utils.spider import transform
from bald_spider.task_manager import TaskManager
from bald_spider.core.processor import Processor
from bald_spider.utils.log import get_logger


class Engine:

    def __init__(self, crawler):
        self.logger = get_logger(self.__class__.__name__)
        self.crawler = crawler
        self.settings = crawler.settings
        self.downloader: Optional[Downloader] = None
        self.scheduler: Optional[Scheduler] = None
        self.processor: Optional[Processor] = None
        self.spider: Optional[Spider] = None
        self.start_requests: Optional[Generator] = None  # Optional 可以是 None
        self.task_manager: TaskManager = TaskManager(self.settings.getint("CONCURRENCY"))
        self.running = False

    async def start_spider(self, spider):
        self.running = True
        self.logger.info(f"bald_spider started. (project name: {self.settings.get('PROJECT_NAME')})")
        self.spider = spider
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.downloader = Downloader(self.crawler)
        if hasattr(self.downloader, "open"):
            self.downloader.open()
        self.processor = Processor(self.crawler)
        self.start_requests = iter(spider.start_requests())
        await self._open_spider()

    async def _open_spider(self):
        crawling = asyncio.create_task(self.crawl())
        # 这里可以做其他的事情
        await crawling

    async def crawl(self):
        """主逻辑"""
        while self.running:
            if (request := await self._get_next_request()) is not None:
                # 请求
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)
                except StopIteration:
                    self.start_requests = None
                except Exception as exc:
                    # 1. 发起请求的 task 要运行完毕
                    # 2. 调度器是否空闲
                    # 3. 下载器是否空闲
                    if not await self._exit():
                        continue
                    self.running = False
                    if self.start_requests is not None:
                        self.logger.error(f"Error during start_requests: {exc}")
                else:
                    # 入队
                    await self.enqueue_request(start_request)
        if not self.running:
            await self.close_spider()

    async def _crawl(self, request):
        # todo 实现并发
        async def crawl_task():
            outputs = await self._fetch(request)
            # 处理 outputs
            if outputs:
                await self._handle_spider_output(outputs)
        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(crawl_task())

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

    async def _handle_spider_output(self, outputs):
        async for spider_output in outputs:
            if isinstance(spider_output, (Request, Item)):
                await self.processor.enqueue(spider_output)
            else:
                raise OutputError(f"{type(self.spider)} must return `Request` or `Item`")

    async def _exit(self):
        if self.scheduler.idle() and self.downloader.idle() and self.task_manager.all_done() and self.processor.idle():
            return True
        return False

    async def close_spider(self):
        await self.downloader.close()
import asyncio
import signal
from typing import Type, Final, Set, Optional

from bald_spider.core.engine import Engine
from bald_spider.event import spider_opened, spider_closed
from bald_spider.exceptions import SpiderTypeError
from bald_spider.spider import Spider
from bald_spider.settings.settings_manager import SettingsManager
from bald_spider.stats_collector import StatsCollector
from bald_spider.subscriber import Subscriber
from bald_spider.extension import ExtensionManager
from bald_spider.utils.project import merge_settings
from bald_spider.utils.log import get_logger

logger = get_logger(__name__)


class Crawler:

    def __init__(self, spider_cls, settings):
        self.spider_cls = spider_cls
        self.spider: Optional[Spider] = None
        self.engine: Optional[Engine] = None
        self.stats: Optional[StatsCollector] = None
        self.subscriber: Optional[Subscriber] = None
        self.extension: Optional[ExtensionManager] = None
        self.settings: SettingsManager = settings.copy()

    async def crawl(self):
        self.subscriber = self._create_subscriber()
        self.spider = self._create_spider()
        self.engine = self._create_engine()
        self.stats = self._create_stats()
        self.extension = self._create_extension()
        await self.engine.start_spider(self.spider)

    @staticmethod
    def _create_subscriber():
        return Subscriber()

    def _create_extension(self):
        extension = ExtensionManager.create_instance(self)
        return extension

    def _create_engine(self) -> Engine:
        engine = Engine(self)
        engine.engine_start()
        return engine

    def _create_stats(self) -> StatsCollector:
        stats = StatsCollector(self)
        return stats

    def _create_spider(self) -> Spider:
        spider = self.spider_cls.create_instance(self)
        self._set_spider(spider)
        return spider

    def _set_spider(self, spider):
        self.subscriber.subscribe(spider.spider_opened, event=spider_opened)
        self.subscriber.subscribe(spider.spider_closed, event=spider_closed)
        merge_settings(spider, self.settings)

    async def close(self, reason="finished"):
        await asyncio.create_task(self.subscriber.notify(spider_closed))
        self.stats.close_spider(self.spider, reason)


class CrawlerProcess:

    def __init__(self, settings=None):
        self.crawlers: Final[Set] = set()
        self._active: Final[Set] = set()
        self.settings = settings

        signal.signal(signal.SIGINT, self._shutdown)

    async def crawl(self, spider: Type[Spider]):
        crawler: Crawler = self._create_crawler(spider)
        self.crawlers.add(crawler)
        task = await self._crawl(crawler)
        self._active.add(task)

    @staticmethod
    async def _crawl(crawler):
        return asyncio.create_task(crawler.crawl())

    async def start(self):
        await asyncio.gather(*self._active)

    def _create_crawler(self, spider_cls) -> Crawler:
        if isinstance(spider_cls, str):
            raise SpiderTypeError(f"{type(self)}.crawl args: String is not supported.")
        crawler = Crawler(spider_cls, self.settings)
        return crawler

    def _shutdown(self, _signum, _frame):
        for crawler in self.crawlers:
            crawler.engine.running = False
            crawler.engine.normal = False
            crawler.stats.close_spider(crawler.spider, "ctrl c")
        logger.warning(f"spiders received `ctrl c` signal, closed.")
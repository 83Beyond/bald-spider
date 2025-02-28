import asyncio

from bald_spider.core.engine import Engine
from bald_spider.utils.project import get_settings
from bald_spider.crawler import CrawlerProcess
from tests.baidu_spider.spiders.baidu import BaiduSpider
from tests.baidu_spider.spiders.baidu2 import BaiduSpider2

async def run():
    # srp 单一职责原则，single responsibility principle
    settings = get_settings()
    process = CrawlerProcess(settings)
    await process.crawl(BaiduSpider)
    # await process.crawl(BaiduSpider2)
    await process.start()

asyncio.run(run())
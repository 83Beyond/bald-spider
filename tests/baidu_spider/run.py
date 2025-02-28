import asyncio

from bald_spider.core.engine import Engine
from bald_spider.utils.project import get_settings
from baidu import BaiduSpider

async def run():
    # srp 单一职责原则，single responsibility principle
    settings = get_settings()
    baidu_spider = BaiduSpider()
    engine = Engine()
    await engine.start_spider(baidu_spider)

asyncio.run(run())
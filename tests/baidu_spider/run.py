import asyncio

from bald_spider.core.engine import Engine
from baidu import BaiduSpider

async def run():

    baidu_spider = BaiduSpider()
    engine = Engine()
    await engine.start_spider(baidu_spider)

asyncio.run(run())
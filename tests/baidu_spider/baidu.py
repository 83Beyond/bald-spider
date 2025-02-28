from bald_spider import Request
from bald_spider.spider import Spider

class BaiduSpider(Spider):

    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]
    # start_url = "https://www.baidu.com"

    async def parse(self, response):
        print("parse", response)
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url)
            yield request


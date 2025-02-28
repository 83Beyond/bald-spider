from bald_spider import Request
from bald_spider.spider import Spider
from items import BaiduItem  # type: ignore

class BaiduSpider(Spider):

    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]

    custom_settings = {"CONCURRENCY": 8}

    def parse(self, response):
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        item = BaiduItem()
        item["url"] = "http://www.baidu.com"
        item["title"] = "百度首页"
        yield item
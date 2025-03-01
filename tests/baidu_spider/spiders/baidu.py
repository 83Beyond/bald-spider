from bald_spider import Request
from bald_spider.spider import Spider
from items import BaiduItem  # type: ignore

class BaiduSpider(Spider):

    start_urls = ["http://www.baidu.com", "http://www.baidu.com"]
    headers = {"User-Agent": ""}

    def parse(self, response):
        for i in range(2):
            url = "http://www.baidu.com"
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        for i in range(2):
            url = "http://www.baidu.com"
            request = Request(url=url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        item = BaiduItem()
        item["url"] = response.url
        item["title"] = response.xpath("//title/text()").get()
        yield item
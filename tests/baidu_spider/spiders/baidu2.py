from bald_spider import Request
from bald_spider.spider import Spider

class BaiduSpider2(Spider):

    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]

    def parse(self, response):
        print("parse2", response)
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        print("parse_page2", response)
        for i in range(10):
            url = "https://www.baidu.com"
            request = Request(url=url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        print("parse_detail2", response)
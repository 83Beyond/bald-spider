from bald_spider import Request
from bald_spider.event import spider_error
from bald_spider.spider import Spider
from items import BaiduItem  # type: ignore

class BaiduSpider(Spider):

    start_urls = ["http://www.baidu.com", "http://www.baidu.com"]
    headers = {"User-Agent": ""}

    @classmethod
    def create_instance(cls, crawler):
        o = cls()
        o.crawler = crawler
        crawler.subscriber.subscribe(o.spider_error, event=spider_error)
        return o

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

    async def spider_error(self, exc, spider):
        print(f"spider error: {exc}, please handle")

    async def spider_opened(self):
        print("spider opened, do something.")

    async def spider_closed(self):
        print("spider closed, do something.")
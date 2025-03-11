from bald_spider import Request
from bald_spider.spider import Spider
from tests.baidu_spider.items import LayItem


class LawSpider(Spider):

    start_urls = ["https://www.66law.cn/question/answer/38-list%d.aspx" % i for i in range(1, 201)]

    def parse(self, response):
        prefix = "https://www.66law.cn"
        li_list = response.xpath("//div[@class='wenda-list bg-ff box-shadow']/ul/li")
        for li in li_list:
            href = li.xpath("./div/a/@href")[0]
            title = li.xpath("./div/a/text()")[0]
            detail_url = prefix + href
            yield Request(
                detail_url,
                callback=self.parse_detail,
                meta={"title": title}
            )

    def parse_detail(self, response):
        li_list = response.xpath("//ul[@style='margin-top: 0px;']/li")
        answer = []
        for li in li_list:
            lawyer = li.xpath(".//div[@class='lawyer']/a/text()")[0]
            if lawyer == "咨询助手":
                continue
            content = li.xpath('./div/p//text()')
            answer.append({"lawyer": lawyer, "answer": ''.join(content)})

        item = LayItem()
        item["title"] = response.meta["title"].strip("\xa0")
        item["answers"] = answer
        item["detail_link"] = response.request.url
        yield item

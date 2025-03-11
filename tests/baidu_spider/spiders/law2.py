from bald_spider import Request
from bald_spider.spider import Spider
from tests.baidu_spider.items import LayItem


class LawSpider(Spider):
    """
    婚姻家庭  完成
    刑事案件  完成
    劳动纠纷  完成
    合同纠纷  完成
    公司企业  完成
    债权债务  完成
    房产纠纷  完成
    交通事故  完成
    继承  完成
    征地拆迁  完成
    建筑工程  完成
    医疗纠纷  完成
    损害赔偿  完成
    行政纠纷  完成
    环境保护  完成
    知识产权  完成
    保险纠纷  完成
    证券投资  完成
    互联网纠纷 完成
    人格尊严 完成
    涉外纠纷 完成
    其他  完成
    """
    start_urls = ["https://www.findlaw.cn/wenda/p229_page%d/" % i for i in range(1, 3)]
    category = "劳动纠纷"

    def parse(self, response):

        ul_list = response.xpath("//ul[@class='consult-list']")
        for ul in ul_list:
            li_list = ul.xpath("./li")
            for li in li_list:
                title = li.xpath("./a/text()")[0]
                link = li.xpath("./a/@href")[0]
                yield Request(
                    link,
                    callback=self.parse_detail,
                    meta={"title": title}
                )

    def parse_detail(self, response):
        li_list = response.xpath("//ul[@class='resolve-list']/li")
        target = []
        for li in li_list:
            lawyer = li.xpath(".//div[@class='resolve-box']/a/text()")
            answer = li.xpath(".//div[@class='resolve-txt']//text()")
            if not lawyer:
                continue
            target.append({"lawyer": lawyer[0], "answer": ''.join(answer)})

        item = LayItem()
        item["title"] = response.meta["title"].strip("")
        item["answers"] = target
        item["detail_link"] = response.request.url
        yield item

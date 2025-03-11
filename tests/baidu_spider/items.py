from bald_spider.items import Field
from bald_spider import Item


class BaiduItem(Item):

    url = Field()
    title = Field()

class LayItem(Item):

    title = Field()
    answers = Field()
    detail_link = Field()
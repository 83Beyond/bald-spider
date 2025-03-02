from bald_spider.items.items import Item


class Pipeline:

    def process_item(self, item: Item, spider):
        raise NotImplementedError

    @classmethod
    def create_instance(cls, crawler):
        return cls()
import random
import os
import json
from motor.motor_asyncio import AsyncIOMotorClient
import aiofiles

from bald_spider.event import spider_closed
from bald_spider.exceptions import ItemDiscard
from bald_spider.utils.log import get_logger


class TestPipeline:

    def process_item(self, item, spider):
        data = item.copy()
        data['title'] = "xxx"
        if random.randint(1, 3) == 1:
            raise ItemDiscard("重复数据")
        return item  # 下一个管道用修改后的，就 return data

    @classmethod
    def create_instance(cls, crawler):
        return cls()


class MongoPipeline:

    def __init__(self, conn, col):
        self.conn = conn
        self.col = col

        self.logger = get_logger(self.__class__.__name__)

    @classmethod
    def create_instance(cls, crawler):
        settings = crawler.settings
        mongo_params = settings.get("MONGO_PARAMS", None)
        db_name = settings.get("DB_NAME")
        project_name = settings.get("PROJECT_NAME")
        conn = AsyncIOMotorClient(**mongo_params) if mongo_params else AsyncIOMotorClient()
        col = conn[db_name][project_name]
        o = cls(conn, col)
        crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
        return o

    async def spider_closed(self, spider):
        self.logger.info("MongoDB closed.")
        self.conn.close()

    async def process_item(self, item, spider):
        await self.col.insert_one(item.to_dict())
        return item


class LayPipeline:

    def __init__(self, category):
        self._data = []
        self.logger = get_logger(self.__class__.__name__)
        self.category = category

    @classmethod
    def create_instance(cls, crawler):
        o = cls(crawler.spider.category)
        crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
        return o

    def process_item(self, item, spider):
        data = {
            "title": item["title"],
            "answers": item["answers"],
            "detail_link": item["detail_link"],
        }
        self._data.append(data)
        return item

    async def spider_closed(self):
        """异步写入数据到 JSON 文件"""
        output_path = f"./zhaofa_data/{self.category}.json"

        async with aiofiles.open(output_path, 'w', encoding='utf-8') as file:
            json_data = json.dumps(self._data, ensure_ascii=False, indent=4)
            await file.write(json_data)  # 异步写入文件
        # output_path = f"./zhaofa_data/{self.category}.json"
        # with open(output_path, 'w', encoding='utf-8') as file:
        #     json.dump(self._data, file, ensure_ascii=False, indent=4)
import random
from asyncio import sleep

from bald_spider.exceptions import IgnoreRequest
from bald_spider.middleware import BaseMiddleware


class TestMiddleware(BaseMiddleware):

    async def process_request(self, request, spider):
        await sleep(0.5)
        if random.randint(1, 5) == 1:
            raise IgnoreRequest("随机忽略请求")

    def process_response(self, request, response, spider):
        print("process_response2",request, response, spider)
        return response

    def process_exception(self, request, exc, spider):
        print("process_exception", request, exc, spider)
        if isinstance(exc, ZeroDivisionError):
            return True  # 内部消化 ZeroDivisionError

class TestMiddleware2(BaseMiddleware):

    def process_response(self, request, response, spider):
        print("process_response1", request, response, spider)
        return response
import random
import requests
import threading

from bald_spider.exceptions import IgnoreRequest
from bald_spider.middleware import BaseMiddleware
from bald_spider.utils.log import get_logger


class ProxyMiddleware(BaseMiddleware):

    USERNAME = ""
    PASSWORD = ""

    def __init__(self, proxy_pool):
        self.proxy_pool = proxy_pool
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"init proxies: {proxy_pool}")
        self.lock = threading.Lock()

    @classmethod
    def create_instance(cls, crawler):
        proxy_pool = [
            "http://%(user)s:%(pwd)s@%(proxy)s/" %
            {"user": cls.USERNAME, "pwd": cls.PASSWORD, "proxy": p} for p in cls._get_proxy()]
        o = cls(proxy_pool)
        return o

    async def process_request(self, request, spider):
        request.proxy = self.get_random_proxy()

    def process_response(self, request, response, spider):
        self.logger.info(f"response: {response}")
        return response

    def process_exception(self, request, exc, spider):
        proxy = request.proxy
        self.remove_proxy(proxy)
        new_proxy = "http://%(user)s:%(pwd)s@%(proxy)s/" % {
            "user": self.USERNAME, "pwd": self.PASSWORD, "proxy": self._get_proxy(1)[0]}
        self.proxy_pool.append(new_proxy)
        self.logger.info(f"成功添加代理{new_proxy}")
        return

    def get_random_proxy(self):
        """随机选择一个代理"""
        with self.lock:
            return random.choice(self.proxy_pool)

    def remove_proxy(self, proxy):
        """移除失效的代理"""
        with self.lock:
            if proxy in self.proxy_pool:
                self.proxy_pool.remove(proxy)
                self.logger.info(f"成功移除不可用代理{proxy}")

    @staticmethod
    def _get_proxy(num=10):
        # 提取代理API接口，获取1个代理IP
        api_url = f""
        # 获取API接口返回的代理IP
        proxy_ip = requests.get(api_url).json()['data']['proxy_list']
        return proxy_ip

class TestMiddleware2(BaseMiddleware):

    def process_response(self, request, response, spider):
        print("process_response1", request, response, spider)
        return response
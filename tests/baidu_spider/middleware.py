from bald_spider.middleware import BaseMiddleware


class TestMiddleware(BaseMiddleware):

    def process_request(self, request, spider):
        pass

    def process_response(self, request):
        pass

    def process_exception(self, request):
        pass

class TestMiddleware2(BaseMiddleware):

    def process_exception(self, request):
        pass
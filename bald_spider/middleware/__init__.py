

class BaseMiddleware:

    def process_request(self, request, spider):
        pass

    def process_response(self, request):
        pass

    def process_exception(self, request):
        pass

    @classmethod
    def create_instance(cls, crawler):
        return cls()
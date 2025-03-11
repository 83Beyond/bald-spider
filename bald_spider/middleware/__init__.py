from bald_spider import Request, Response


class BaseMiddleware:

    def process_request(self, request, spider) -> None | Request | Response:
        pass

    def process_response(self, request, response, spider) -> Request | Response:
        pass

    def process_exception(self, request, exc, spider) -> None | Request | Response:
        pass

    @classmethod
    def create_instance(cls, crawler):
        return cls()

from bald_spider.exceptions import IgnoreRequest
from bald_spider.utils.log import get_logger


class ResponseFilter:

    def __init__(self, allowed_codes, log_level):
        self.allowed_codes = allowed_codes
        self.logger = get_logger(self.__class__.__name__, log_level)

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            allowed_codes=crawler.settings.getlist("ALLOWED_CODES"),
            log_level=crawler.settings.get("LOG_LEVEL")
        )
        return o

    def process_response(self, request, response, spider):
        if 200 <= response.status < 300:
            return response
        if response.status in self.allowed_codes:
            return response
        raise IgnoreRequest(f"response_status/non-200")
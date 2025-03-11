from bald_spider.utils.log import get_logger


class ResponseCodeStats:

    def __init__(self, stats, log_level):
        self.logger = get_logger(self.__class__.__name__, log_level)
        self.stats = stats

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            stats=crawler.stats,
            log_level=crawler.settings.get("LOG_LEVEL")
        )
        return o

    def process_response(self, _request, response, _spider):
        self.stats.inc_value(f"stats_code/count/{response.status}")
        self.logger.debug(f"Got response from <{response.status} {response.url}>")
        return response

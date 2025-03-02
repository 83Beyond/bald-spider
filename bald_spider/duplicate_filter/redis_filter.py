import redis
from redis import Redis

from bald_spider.duplicate_filter import BaseFilter
from bald_spider.utils.log import get_logger
from bald_spider.stats_collector import StatsCollector


class RedisFilter(BaseFilter):

    def __init__(
        self,
        redis_key: str,
        client: Redis,
        debug: bool,
        save_fp: bool,
        stats: StatsCollector,
        log_level: str
    ):
        logger = get_logger(f"{self}", log_level)
        super().__init__(logger, stats, debug)
        self.redis_key = redis_key
        self.redis = client
        self.save_fp = save_fp

    @classmethod
    def create_instance(cls, crawler):
        redis_url = crawler.settings.get("REDIS_URL")
        decode_responses = crawler.settings.getbool("DECODE_RESPONSES")
        redis_client = redis.from_url(redis_url, decode_responses=decode_responses)
        o = cls(
            redis_key=f"{crawler.settings.get('PROJECT_NAME')}:{crawler.settings.get('REDIS_KEY')}",
            client=redis_client,
            debug=crawler.settings.getbool("FILTER_DEBUG"),
            save_fp=crawler.settings.getbool("SAVE_FP"),
            stats=crawler.stats,
            log_level=crawler.settings.get("LOG_LEVEL")
        )
        return o

    def add(self, fp: str):
        self.redis.sadd(self.redis_key, fp)

    def __contains__(self, item):
        return self.redis.sismember(self.redis_key, item)

    async def closed(self):
        if not self.save_fp:
            self.redis.delete(self.redis_key)
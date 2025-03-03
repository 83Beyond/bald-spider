import asyncio
from asyncio import PriorityQueue, TimeoutError
from typing import Optional

from bald_spider import Request


class SpiderPriorityQueue(PriorityQueue):

    def __init__(self, maxsize=0):
        super(SpiderPriorityQueue, self).__init__(maxsize=maxsize)

    async def get(self) -> Optional[Request]:
        f = super().get()
        try:
            return await asyncio.wait_for(f, timeout=0.1)
        except TimeoutError:
            return None
import random
import asyncio

import requests


class Downloader:

    def __init__(self):
        pass

    async def fetch(self, request):
        return await self.download(request)

    async def download(self, request):
        # response = requests.get(request.url)
        # print(response)
        await asyncio.sleep(random.uniform(0, 1))
        return "result"
from typing import Optional
import httpx

from bald_spider.core.downloader import DownloaderBase
from bald_spider import Response


class HTTPXDownloader(DownloaderBase):

    def __init__(self, crawler):
        super().__init__(crawler)
        self._client: Optional[httpx.AsyncClient()] = None
        self._timeout: Optional[httpx.Timeout] = None

    def open(self):
        super().open()
        request_time = self.crawler.settings.getint("REQUEST_TIMEOUT")
        self._timeout = httpx.Timeout(timeout=request_time)

    async def fetch(self, request) -> Optional[Response]:
        async with self._active(request):
            response = await self.download(request)
            return response

    async def download(self, request) -> Optional[Response]:
        try:
            proxies = request.proxy
            async with httpx.AsyncClient(timeout=self._timeout, proxy=proxies) as client:
                self.logger.debug(f"request downloading: {request.url}, method: {request.method}")
                response = await client.request(
                    request.method, request.url, headers=request.headers, cookies=request.cookies, data=request.body
                )
                body = await response.aread()
        except Exception as exc:
            self.logger.error(f"Error during request: {exc}")
            raise exc
        return self.structure_response(request, response, body)

    @staticmethod
    def structure_response(request, response, body) -> Response:
        return Response(
            url=response.url,
            headers=dict(response.headers),
            status=response.status_code,
            body=body,
            request=request
        )

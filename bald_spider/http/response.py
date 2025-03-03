from typing import Dict
import ujson
import re
from parsel import Selector
from urllib.parse import urljoin as _urljoin

from bald_spider import Request
from bald_spider.exceptions import DecodeError


class Response:

    def __init__(
            self,
            url: str,
            *,
            request: Request,
            headers: Dict,
            body: bytes = b"",
            status: int = 200,
    ):
        self.url = url
        self.request = request
        self.headers = headers
        self.body = body
        self.status = status
        self.encoding = request.encoding
        self._text_cache = None
        self._json_cache = None
        self._selector = None

    @property
    def text(self):  # 什么时候用，就什么时候生成
        if self._text_cache:  # 缓存
            return self._text_cache
        try:
            self._text_cache = self.body.decode(self.encoding)
        except UnicodeDecodeError:
            try:
                _encoding_re = re.compile(r"charset=([\w-]+)", flags=re.I)
                _encoding_string = self.headers.get("Content-Type", "") or self.headers.get("content-type", "")
                _encoding = _encoding_re.search(_encoding_string)
                if _encoding:
                    _encoding = _encoding.group(1)
                    self._text_cache = self.body.decode(_encoding)
                else:
                    raise DecodeError(f"{self.request} {self.request.encoding} error.")
            except UnicodeDecodeError as exc:
                raise UnicodeDecodeError(
                    exc.encoding, exc.object, exc.start, exc.end, f"{self.request}"
                )
        return self._text_cache

    def xpath(self, xpath_string):
        if self._selector is None:
            self._selector = Selector(self.text)
        return self._selector.xpath(xpath_string)

    def json(self):
        if self._json_cache:
            return self._json_cache
        self._json_cache = ujson.loads(self.text)
        return self._json_cache

    def urljoin(self, url):
        return _urljoin(self.url, url)

    def __str__(self):
        return f"<{self.status}> {self.url}"
    
    @property
    def meta(self):
        return self.request.meta

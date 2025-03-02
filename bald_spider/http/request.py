from typing import Dict, Optional, Callable


class Request:

    def __init__(
            self,
            url: str,
            *,  # 后面参数是强制关键字参数
            headers: Optional[Dict] = None,
            callback: Optional[Callable] = None,
            priority: int = 0,
            method: str = "GET",
            cookies: Optional[Dict] = None,
            proxy: Optional[Dict] = None,
            body="",
            encoding="utf-8",
            meta: Optional[Dict] = None
    ):
        self.url = url
        self.headers = headers if headers else {}
        self.callback = callback
        self.priority = priority
        self.method = method
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.encoding = encoding
        self._meta = meta if meta is not None else {}

    def __str__(self):
        return f"{self.url} {self.method}"

    def __lt__(self, other):
        return self.priority < other.priority

    @property
    def meta(self):
        return self._meta
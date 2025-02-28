

class Spider:

    def __init__(self):
        if not hasattr(self, "start_urls"):
            self.start_urls = []

    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield url
        else:  # 兼容 spider 中只有 start_url 的情况
            if hasattr(self, "start_url") and isinstance(getattr(self, "start_url"), str):
                yield getattr(self, "start_url")

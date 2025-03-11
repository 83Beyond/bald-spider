from collections import defaultdict
from typing import Dict, Set, Callable, Coroutine
import asyncio
from inspect import iscoroutinefunction

from bald_spider.exceptions import ReceiverTypeError


class Subscriber:

    def __init__(self):
        self._subscriber: Dict[str, Set[Callable[..., Coroutine]]] = defaultdict(set)

    def subscribe(
            self,
            receiver: Callable[..., Coroutine],
            *,
            event: str
    ) -> None:
        if not iscoroutinefunction(receiver):
            raise ReceiverTypeError(f"{receiver.__qualname__} must be a coroutine function.")
        self._subscriber[event].add(receiver)

    def unsubscribe(
            self,
            receiver: Callable[..., Coroutine],
            *,
            event: str
    ) -> None:
        self._subscriber[event].discard(receiver)

    async def notify(self, event: str, *args, **kwargs):
        for receiver in self._subscriber[event]:
            asyncio.create_task(receiver(*args, **kwargs))

from collections import defaultdict
from typing import Dict, Set, Callable, Coroutine
import asyncio


class Subscriber:

    def __init__(self):
        self._subscriber: Dict[str, Set[Callable[..., Coroutine]]] = defaultdict(set)

    def subscribe(
            self,
            receiver: Callable[..., Coroutine],
            *,
            event: str
    ) -> None:
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
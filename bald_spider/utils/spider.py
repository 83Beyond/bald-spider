from inspect import isgenerator, isasyncgen
from typing import Union, AsyncGenerator, Generator

from bald_spider import Response, Request, Item
from bald_spider.exceptions import TransformTypeError

T = Union[Request, Item]
SpiderOutputType = Union[Generator[T, None, None], AsyncGenerator[T, None]]


async def transform(
        func_result: SpiderOutputType,
        response: Response
):

    def set_request(t: T) -> T:
        if isinstance(t, Request):
            t.meta["depth"] = response.meta["depth"]
        return t

    try:
        if isgenerator(func_result):
            for r in func_result:
                yield set_request(r)
        elif isasyncgen(func_result):
            async for r in func_result:
                yield set_request(r)
        else:
            raise TransformTypeError("callback return value must be `generator` or `async generator`")
    except Exception as exc:
        yield exc

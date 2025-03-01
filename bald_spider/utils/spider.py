from inspect import isgenerator, isasyncgen

from bald_spider.exceptions import TransformTypeError


async def transform(func_result):
    try:
        if isgenerator(func_result):
            for r in func_result:
                yield r
        elif isasyncgen(func_result):
            async for r in func_result:
                yield r
        else:
            raise TransformTypeError("callback return value must be `generator` or `async generator`")
    except Exception as exc:
        yield exc
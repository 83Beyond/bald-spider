import asyncio
from asyncio import (Semaphore,
                     BoundedSemaphore)  # 有界的，如果到界了，再 release 就会报错

semaphore = Semaphore(5)

async def demo():
    await semaphore.acquire()
    print(11111)
    await semaphore.acquire()
    print(22222)
    await semaphore.acquire()
    print(33333)
    await semaphore.acquire()
    print(44444)
    await semaphore.acquire()
    print(55555)
    await semaphore.acquire()
    print(66666)


asyncio.run(demo())
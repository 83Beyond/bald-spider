from asyncio import PriorityQueue
from bald_spider import Request

pq = PriorityQueue()

item1 = Request(url="111", priority=1)
item2 = Request(url="222", priority=1)
item3 = Request(url="333", priority=1)


pq.put_nowait(item1)
pq.put_nowait(item2)
pq.put_nowait(item3)

while not pq.empty():
    print(pq.get_nowait())
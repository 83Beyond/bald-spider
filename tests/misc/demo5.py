from timeit import timeit
s = set()

def demo():
    s.add(1)
    s.remove(1)

def run():
    print(timeit(demo, number=10000000))


run()
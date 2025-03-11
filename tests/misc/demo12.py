a = {"1": 1}
b = a.setdefault("1", 0)
print(a)
print(b)
b = a.pop("2", 2)
print(a)
print(b)
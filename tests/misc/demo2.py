from tests.baidu_spider import settings

for name in dir(settings):
    if name.isupper():
        print(getattr(settings, name))
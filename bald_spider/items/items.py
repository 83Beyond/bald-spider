from collections.abc import MutableMapping
from copy import deepcopy
from pprint import pformat

from bald_spider.items import Field, ItemMeta



class Item(MutableMapping, metaclass=ItemMeta):

    FIELDS: dict

    def __init__(self):
        self._values = {}

    def __setitem__(self, key, value):
        if key in self.FIELDS:
            self._values[key] = value
        else:
            raise KeyError(f"{self.__class__.__name__} does not support field: {key}")

    def __getitem__(self, key):
        return self._values[key]

    def __delitem__(self, key):
        del self._values[key]

    def __setattr__(self, key, value):
        if not key.startswith("_"):  # self._values 也会进这里
            raise AttributeError(f"use item[{key!r}] = {value!r} to set field value.")
        super().__setattr__(key, value)

    def __getattr__(self, item):
        raise AttributeError(
            f"{self.__class__.__name__} does not support field: {item}. "
            f"please add the `{item}` field to the {self.__class__.__name__}, "
            f"and use item[{item!r}] to get field value.")

    def __getattribute__(self, item):
        field = super().__getattribute__("FIELDS")
        if item in field:
            raise AttributeError(f"use item[{item!r}] to get field value.")
        else:
            return super().__getattribute__(item)

    def __str__(self):
        return pformat(dict(self))

    __repr__ = __str__

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def to_dict(self):
        return dict(self)

    def copy(self):
        return deepcopy(self)

if __name__ == '__main__':
    class TestItem(Item):
        url = Field()
        title = Field()
    class TestItem2(Item):
        name = Field()
    test_item = TestItem()
    test_item2 = TestItem2()
    # test_item.a = 1
    # print(test_item2.name)
    print(test_item2.aaaaaa)
    # test_item["aaa"] = 1
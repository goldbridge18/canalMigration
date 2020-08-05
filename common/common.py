
from collections import abc


def findUpdatedFiled(filedsDict):
    filedsList = []
    for k, v in filedsDict.items():
        if v == True:
            filedsList.append(k)
    return filedsList


# 迭代器；json字符串；嵌套字典的数据读取
def nestedDictIter(nested):
    for key, value in nested.items():
        if isinstance(key, bytes):
            key = key.decode()
        if isinstance(key, int):
            key = "{key}".format(key=key)
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, int):
            value = "{value}".format(value=value)
        if isinstance(value, abc.Mapping):
            # yield from nested_dict_iter(value)
            for k2 in nestedDictIter(value):
                if isinstance(k2, int):
                    k2 = str(k2)
                yield (key,) + k2

        else:
            yield key, value


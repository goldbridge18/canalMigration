
from collections import abc


def findUpdatedFiled(filedsDict,filterFiled = ""):
    filedsList = []
    for k, v in filedsDict.items():
        if  v == True:
            if k == filterFiled:
                pass
            else:
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


xxx = '{"mouseEvent":{"eventType":"","targetId":"","eventData":{}},"isPlay":true,"progress":[1,0,0]}'
xxx = '{"at":"改个","a":"op","d":"editor","v":71,"src":"e386636486ab273d943ca05c03bcb455","seq":72,"op":[{"p":["code",0],"sd":"🏘️🏘️🏬🎡🎠🚀🚀🏨🏨🗺️🚧🚝🚋🚧🏤🏦🏛️🏛️😏😏😔"}]}'
import json
print(json.loads(xxx))
for i in nestedDictIter(json.loads(xxx)):
    print(i)


def getBinlogValues(updateDic,filterFilde = ""):
    '''
    获取binlog的数据信息
    :param updateDic:
    :return: 两个元素的list类型数据 index:0 是key 的列表 ，index：1是value的列表
    '''
    keyList = []
    valueList = []

    keyList.append("operation_type")
    valueList.append(updateDic["event_type"])

    keyList.append("execute_time")
    valueList.append(updateDic["execute_time"])

    if updateDic["event_type"] == 2:  # 更新
        for k, v in updateDic["data"]["after"].items():
            if k == filterFilde :
                pass
            elif v == '' and updateDic["updated_fields"][k] == False:
                pass
            elif v == '' and updateDic["updated_fields"][k] == True:
                v = "NULL"
                pass
                # keyList.append(k)
                # valueList.append(v)
            else:
                keyList.append(k)
                valueList.append(v)

    elif updateDic["event_type"] == 1 or updateDic["event_type"] == 3:  # insert
        for k, v in updateDic["data"].items():
            if k == filterFilde:
                pass
            elif v == '' :
                # v = "NULL"
                pass
                # keyList.append(k)
                # valueList.append(v)
            else:
                keyList.append(k)
                valueList.append(v)

    else:
        pass

    totalList = []  #index:0 是key 的列表 ，index：1是value的列表
    totalList.append(keyList)
    totalList.append(valueList)
    # print("getBinlogValues--->",totalList)
    return totalList



import time
import pymysql
import re, datetime, json
import phpserialize

from collections import abc
from common.common import nestedDictIter


# #  处理phpjson、json 循环嵌套--转换成dict
# def jsonToDictToSql(jsonStr, tableName, jsonType="json"):
#     '''
#     :param jsonStr:
#     :param tableName:
#     :param jsonType: 默认json ； phpjson
#     :return: 字典
#     '''
#     # 转字典
#     if jsonType == "json":
#         jsonToDict = json.loads(jsonStr)
#         # jsonToDict = jsonStr
#     elif jsonType == "phpjson":
#         strToByte = bytes(jsonStr, encoding="utf8")
#         byteToDict = phpserialize.loads(strToByte)
#         jsonToDict = byteToDict
#
#     keyList = []
#     valuesList = []
#
#     '''
#     调用nested_dict_iter函数 yield
#     读取嵌套字典的数据
#     '''
#     for i in nestedDictIter(jsonToDict):
#         keyname = "_".join(i[:-1])
#         valuename = "{value}".format(value=i[-1])
#
#         keyList.append(keyname)
#         valuesList.append(valuename)
#
#     dict_data = dict(zip(keyList, valuesList))
#     return dict_data


# 处理field josn格式的字符串，反序列化，返回list数据
def jsonToList(jsonStr, fieldName="", jsonType="json"):
    '''
    :param jsonStr:
    :param fieldName:
    :param jsonType: 默认json ； phpjson
    :return: list index:0 keyname index:1-n values
    '''
    # 转字典
    # print("---------------->:",jsonStr)
    if jsonType == "json":
        jsonToDict = json.loads(jsonStr)
        # jsonToDict = jsonStr
    elif jsonType == "phpjson":
        phpseriTostr = str(phpserialize.loads(jsonStr.encode(), decode_strings=True))

        reStr = re.sub('(?<!^)}(?!$)', "]",
                       re.sub('(?<!^){(?!$)', "[", re.sub('[0-9]+:', '', re.sub('[0-9]+:', '', phpseriTostr)))).replace(
            "\'", "\"").replace(" ", "")
        try:
            jsonToDict = json.loads(reStr.replace("None","0"))
        except Exception as e:
            with open("./logs/parse_jsonerr.txt","a+") as f:
                f.write("\n")
                f.write(reStr)

    keyList = []
    valuesList = []
    totalList = []
    '''
    调用nested_dict_iter函数 yield
    读取嵌套字典的数据
    '''
    for i in nestedDictIter(jsonToDict):
        keyname = "json_" + "".join(i[:-1])
        if jsonType == "json":
            keyname = ("json_" + "_".join(i[:-1])).replace("-","_")

        valuename = i[-1]
        if isinstance(valuename,list) and len(valuename) == 0:
            valuename = ""
        keyList.append(keyname)
        valuesList.append(valuename)

    totalList.append(keyList)
    valListLen = len(valuesList)
    valListElementLen = len(valuesList[0])
    try:
        if jsonType == "phpjson":
            for i in range(valListElementLen):
                tmpList = []
                for j in range(valListLen):
                    tmpList.append(valuesList[j][i])

                totalList.append(tmpList)
            # print(totalList)
        else:
            totalList.append(valuesList)
    except Exception as e:
        # print("---------------->",jsonStr)
        with open("./logs/error_json.txt","a+") as f:
            f.write("\n")
            f.write(jsonStr)
        return []
    return totalList

def getBinlogValues(updateDic):
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
            keyList.append(k)
            valueList.append(v)

    elif updateDic["event_type"] == 1 or updateDic["event_type"] == 3:  # insert
        for k, v in updateDic["data"].items():
            keyList.append(k)
            valueList.append(v)

    else:
        pass

    totalList = []  #index:0 是key 的列表 ，index：1是value的列表
    totalList.append(keyList)
    totalList.append(valueList)
    print("getBinlogValues--->",totalList)
    return totalList


# 处理update\insert语句
def updateAndInsertSql(updateDic,tableName):
    '''
    记录中不需要反序列化的，生成inser语句
    :param updateDic:
    :param tableName:
    :return:
    '''

    keyList = getBinlogValues(updateDic)[0]
    valuesList = getBinlogValues(updateDic)[1]

    filedsSqlList = str(keyList).replace('[', '(').replace(']', ')').replace('\'', '')
    valuesSqlList = str(valuesList).replace('[', '(').replace(']', ')')

    SQL = "insert into " + tableName + " " + filedsSqlList + " values " + valuesSqlList + ";"
    print("function：updateAndInsertSql---> ",SQL)
    return SQL


def includeJsonSql(updateDic,hapTableName ,filedName, jsonType,num):
    '''
    反序列化 json phpjson 后，生成insert语句
    :param updateDic:
    :param filedName:
    :param num:
    :return:  list
    '''
    keyList = []
    valuesList = []
    filedsSqlList = ""
    valuesSqlList = ""
    jsontoList = []
    sqlList = []

    keyList.append("operation_type")
    valuesList.append(updateDic["event_type"])

    keyList.append("execute_time")
    valuesList.append(updateDic["execute_time"])

    if num == 2:  # 更新
        for k, v in updateDic["data"]["after"].items():
            keyList.append(k)
            valuesList.append(v)

        filedsSqlList = str(keyList).replace('[', '(').replace(']', ')').replace('\'', '')
        valuesSqlList = str(valuesList).replace('[', '(').replace(']', ')')

    elif num == 1:  # insert
        for k, v in updateDic["data"].items():
            if k == filedName:
                # print(k)
                jsontoList = jsonToList(v, k, jsonType= jsonType)

            else:
                keyList.append(k)
                valuesList.append(v)
    else:
        pass

    jsontoListLen = len(jsontoList)

    if len(jsontoList) != 0:
        tmpkeyList = keyList + jsontoList[0]
        # print("tmpfiledsSqlList------>: ",tmpkeyList)
        filedsSqlList = str(tmpkeyList).replace('[', '(').replace(']', ')').replace('\'', '')

        for i in range(jsontoListLen - 1):
            tempvaluesSqlList = valuesList
            tempvaluesSqlList = tempvaluesSqlList + jsontoList[i + 1]
            valuesSqlList = str(tempvaluesSqlList).replace('[', '(').replace(']', ')')
            #

            SQL = "insert into " + hapTableName + " " + filedsSqlList + " values " + valuesSqlList + ";"
            sqlList.append(SQL)


    else:
        SQL = "insert into " + hapTableName + " " + filedsSqlList + " values " + valuesSqlList + ";"
        sqlList.append(SQL)

    return sqlList


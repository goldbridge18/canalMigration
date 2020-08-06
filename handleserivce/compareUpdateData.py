import re,os
import phpserialize
from collections import abc
import json,os,sys

from common.common import findUpdatedFiled
from common.loggerout import writeLogContext

def jsonToDict(jsonStr, jsonType="json"):
    jsonToDict = dict()
    if jsonType == "json":
        jsonToDict = json.loads(jsonStr)
        # jsonToDict = jsonStr
    elif jsonType == "phpjson":
        # print("------jsonToDict--------")
        try:
            phpseriTostr = str(phpserialize.loads(jsonStr.encode(), decode_strings=True))

            reStr = re.sub('(?<!^)}(?!$)', "]",
                           re.sub('(?<!^){(?!$)', "[", re.sub('[0-9]+:', '', re.sub('[0-9]+:', '', phpseriTostr)))).replace(
                "\'", "\"").replace(" ", "")

            tmpJsonToDict = json.loads(reStr)

            for k, v in tmpJsonToDict.items():
                jsonToDict["josn_" + k] = v

        except ValueError as e:
            print("反序列的值有问题")
            return 0

    return jsonToDict


def getListDefferSet(before, after):
    '''

    :param before:
    :param after:
    :return:
    '''
    beforeDict = jsonToDict(before, "phpjson")
    afterDict = jsonToDict(after, "phpjson")
    tmpBefore = []
    tmpAfter = []

    #
    if beforeDict == 0  or afterDict == 0 or before == after:
        # add log put out
        return []
    # 对比before 和after的 字典值，并取得list的值得交集
    for k, v in beforeDict.items():
        tmpBefore.append(k)
    for k, v in afterDict.items():
        tmpAfter.append(k)

    joinFieldsList = [item for item in tmpBefore if item in tmpAfter] #交集
    defferFieldsList = list(set(tmpAfter) ^ set(tmpBefore)) #差集

    fieldsList = []
    valList = []
    totalList = []

    for name in joinFieldsList:
        ret = list(set(afterDict[name]) ^ set(beforeDict[name]))
        if len(ret) < 1:
            fieldsList.append(name)
            valList.append(beforeDict[name][-1])
        else:
            fieldsList.append(name)
            valList.append(ret[0])
    for addName in defferFieldsList:
        newVal = afterDict[addName]

        fieldsList.append(addName)
        valList.append(newVal[0])

    totalList.append(fieldsList)
    totalList.append(valList)
    print(os.path.basename(__file__),"--------->:",totalList)
    return totalList


def parseUpdateJsonToSql(updateDic,filedName,hadTableName):
    '''
    only jsonType="phpjson"
    只针对phpjson 的值做更改，对更改前后的值对比生成差异部分，返回sql语句
    :param updateDic:
    :param filedName:
    :param num:
    :return:
    '''
    keyList = []
    valuesList = []
    filedsSqlList = ""
    valuesSqlList = ""
    jsontoList = []
    sqlList = []
    # print("-------> ", updateDic["data"])

    for k, v in updateDic["data"]["after"].items():
        if k != filedName:
            keyList.append(k)
            valuesList.append(v)
    keyList.append("operation_type")
    valuesList.append(updateDic["event_type"])

    keyList.append("execute_time")
    valuesList.append(updateDic["execute_time"])

    jsontoList = getListDefferSet(updateDic["data"]["before"][filedName],
                                  updateDic["data"]["after"][filedName])
    # print(getListDefferSet(before, after))
    # print("jsontoList------->:",jsontoList)
    # if jsontoList == False:
    #     return []

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
            # print("valuesSqlList001------>:",valuesSqlList)
            # print("filedsSqlList001------>:",filedsSqlList)
            SQL = "insert into " + hadTableName + " " + filedsSqlList + " values " + valuesSqlList + ";"
            sqlList.append(SQL)

    else:
        filedsSqlList = str(keyList).replace('[', '(').replace(']', ')').replace('\'', '')
        valuesSqlList = str(valuesList).replace('[', '(').replace(']', ')')
        SQL = "insert into " + updateDic["table"] + " " + filedsSqlList + " values " + valuesSqlList + ";"
        sqlList.append(SQL)


    return sqlList



def setUpdatedFieldValue(updateDic,filedName=''):
    '''
    统计所有update的状态字段，返回list
    :param updateDic:
    :param filedName:
    :return: 值为list index 0位key index 1位value
    '''
    totalList = []
    # print("-setUpdatedFieldValue--------",updateDic)
    if filedName != '' and updateDic["event_type"] == 2:
        jsontoList = getListDefferSet(updateDic["data"]["before"][filedName],
                                  updateDic["data"]["after"][filedName])[0]

        filedsName = findUpdatedFiled(updateDic["updated_fields"])
        delIndex = [index for index,val in enumerate(filedsName) if val == filedName ]
        del filedsName[delIndex[0]]
        tmpList = filedsName + jsontoList

        for value in tmpList:
            totalList.append("is_"+value)

        # print("++++++++++++++++1",totalList)
        # # return totalList
    else:
        tmpList = findUpdatedFiled(updateDic["updated_fields"])
        for value in tmpList:
            totalList.append("is_" + value)
        # print("++++++++++++++++2",totalList)

    # filedsAndValue = dict()
    # for key in totalList:
    #     filedsAndValue[key] = 1 #1代表ture 0代表flase
    # print(filedsAndValue)
    keyList = []
    valList = []
    AllTotalList = []
    for v in totalList:
        keyList.append(v)
        valList.append(1)
    AllTotalList.append(keyList)
    AllTotalList.append(valList)
    return AllTotalList

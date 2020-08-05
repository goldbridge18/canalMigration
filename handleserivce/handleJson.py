
import time
import pymysql
import re, datetime, json
import phpserialize

from collections import abc
from common.common import nestedDictIter,getBinlogValues
from handleserivce.compareUpdateData import setUpdatedFieldValue
from common.loggerout import writeLogContext

# 处理field josn格式的字符串，反序列化，返回list数据
def jsonToList(jsonStr, fieldName="", jsonType="json"):
    '''
    :param jsonStr:
    :param fieldName:
    :param jsonType: 默认json ； phpjson
    :return: list index:0 keyname index:1-n values
    '''
    # 转字典
    # print("---------转字典------->:",jsonStr)
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
        print("---------------->",e)
        with open("./logs/error_json.txt","a+") as f:
            f.write("\n")
            f.write("{a} : {b}".format(a =e ,b=jsonStr))
        return []
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
    # print("function：updateAndInsertSql---> ",SQL)
    return SQL


def handleJsonData():
    pass

def handleInJsonToList(updateDic, jsonType = "",filedName = ""):
    '''
    合并反序列化之后的和字段的合并
    :param updateDic:
    :param jsonType:
    :param filedName:
    :return:  返回一个数组 index=0是fileds index=1 是values,values是一个list  例如：返回值 [[..],[[..],[..]]]
    '''
    parseJsonList = []
    valList = []
    totalList = []
    filedsAndValueList = getBinlogValues(updateDic,filedName)# 获取binlog中的所有值，返回一个数组 index=0是fileds index=1 是values

    if filedName != "" and updateDic["event_type"] == 2:  # insert

        parseJsonList = jsonToList(updateDic["data"]["after"][filedName], filedName, jsonType=jsonType)

    elif filedName != "" and (updateDic["event_type"] == 1 or updateDic["event_type"] == 3):
        parseJsonList = jsonToList(updateDic["data"][filedName], filedName, jsonType=jsonType)


    if len(parseJsonList) != 0:
        keyList = filedsAndValueList[0] + parseJsonList[0]
        for i in range(len(parseJsonList) - 1):

            valList.append(filedsAndValueList[1] + parseJsonList[i + 1])

        totalList.append(keyList)
        totalList.append(valList)

    else:
        totalList.append(filedsAndValueList[0])
        tmpList = []
        tmpList.append(filedsAndValueList[1])
        totalList.append(tmpList)

    return totalList

def mergeAllFiledValue(updateDic, jsonType="", filedName=""):
    '''
    把updated 的字段及值合并到数据List中
    :param updateDic:
    :param jsonType:
    :param filedName:
    :return:
    '''

    totalList = []
    valueList = []
    filedList = []

    if updateDic["event_type"] == 2:

        updatedList = setUpdatedFieldValue(updateDic, filedName) #获取key为true的值

        if filedName == "":
           filedList =  getBinlogValues(updateDic,filedName)[0] + updatedList[0]
           valueList =  getBinlogValues(updateDic,filedName)[1] + updatedList[1]

           totalList.append(filedList)
           totalList.append(valueList)
        else:
            filedList = handleInJsonToList(updateDic, jsonType, filedName)[0] + getBinlogValues(updateDic,filedName)[0] + updatedList[0]
            # print("--------111---",handleInJsonToList(updateDic, jsonType, filedName))
            # print("--------111---",handleInJsonToList(updateDic, jsonType, filedName)[1])

            for i in  handleInJsonToList(updateDic, jsonType, filedName)[1]:

                valueList.append(getBinlogValues(updateDic,filedName)[1] + updatedList[1])
            totalList.append(filedList)
            totalList.append(valueList)
    else:

        totalList = handleInJsonToList(updateDic, jsonType,filedName )

    return totalList


def getSql(updateDic, tableName,jsonType="", filedName=""):
    '''

    :param updateDic:
    :param tableName:
    :param jsonType:
    :param filedName:
    :return:  list
    '''
    sqlList = []
    tmpList = mergeAllFiledValue(updateDic, jsonType, filedName)
    # print("++++++++++++++",tmpList)
    filedList = tmpList[0]
    valueList = tmpList[1]

    fields = str(filedList).replace("[", "(").replace("]", ")").replace("'", "`")
    values = str(valueList).replace("[[", "(").replace("]]", ")").replace("[", "(").replace("]", ")")
    sql = "insert into " + tableName +fields + " values" + values

    sqlList.append(sql)
    return sqlList



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
        filedsSqlList = str(tmpkeyList).replace('[', '(').replace(']', ')').replace('\'', '')

        for i in range(jsontoListLen - 1):
            tempvaluesSqlList = valuesList
            tempvaluesSqlList = tempvaluesSqlList + jsontoList[i + 1]
            valuesSqlList = str(tempvaluesSqlList).replace('[', '(').replace(']', ')')

            SQL = "insert into " + hapTableName + " " + filedsSqlList + " values " + valuesSqlList + ";"
            sqlList.append(SQL)
    else:
        SQL = "insert into " + hapTableName + " " + filedsSqlList + " values " + valuesSqlList + ";"
        sqlList.append(SQL)

    return sqlList


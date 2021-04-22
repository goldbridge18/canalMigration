# -*- coding:utf-8 -*-
import json,datetime
from collections import abc
from kafkaserver.commServer import  handleStringJson
from kafkaserver.commServer import  handleJsonTosql
from kafkaserver.commServer import  handleStringJson
from common.loggerout import writeLogContext
from  kafkaserver.commServer import nestedMongKafkaJsonToList
#处理 ClassDetails_xx_xx_xx ---------------------------------------------------------------------

def handleDetailsKeyData(string,operationType = "insert"):
    '''
    用于处理 key是Data中的值
    :param string:
    :return: 返回值 [{},{},{}]
    '''
    delKey = ["NewGroupNum_List","Json","chatmes"]
    KeyMergeValue = ["DelGroupNum_List","affectedusers"]
    KeyResetName = ["Area","PolicyNum_List","OSize"]
    maxNum = 0
    totalList = []
    tmpTotalList = []
    tmpOtherList = []
    totalDictInsertList = []

    #递归 获取dict的value
    if operationType == "insert":
        data = string
    elif operationType == "update":
        data = string["Value"]

    try:
        for i in data:
            # print("----------xxxxx--------", i)
            if i["Name"] not in delKey:
                count = 1
                for val in nestedMongKafkaJsonToList(i):

                    if i["Name"] in KeyMergeValue: # 把 [groupid:1,groupid:2,groupid:3] 枚举类型的合并
                        if count%2 != 0:
                            val = i["Name"] + "_" + val
                            # print(val)
                        tmpOtherList.append(val)
                        count +=1
                    elif i["Name"] in KeyResetName:
                        if count % 2 != 0:
                            val = i["Name"] + "_" + val
                            # print(val)
                        tmpTotalList.append(val)
                        count += 1
                    else:
                        tmpTotalList.append(val)
    except Exception as e:
        writeLogContext(e,"info")
        writeLogContext(string,"info")
    #dict 值合并
    if len(tmpOtherList) != 0 :
        xx = str([tmpOtherList[i] for i in range(len(tmpOtherList)) if i%2 != 0]).replace("[","").replace("]","")
        tmpTotalList.append(tmpOtherList[0])
        tmpTotalList.append(xx)

    num = [x for x in range(len(tmpTotalList)) if x%2 == 0]
    for i in num:
        totalDictInsertList.append({tmpTotalList[i]:tmpTotalList[i+1]})

    keyList = [k for val in totalDictInsertList for k in val]
    #keyList 值去重
    notDuplicationKeyList = list(dict.fromkeys(keyList)) #利用dict的 不可重复性

    tmpCommKeyDict = {} #没有重复key的
    tmpMulKeyDict = {}  #有重复key的

    #在list里没有重复的key值 ；找到notDuplicationKeyList中key (val) 在keyList中的index下标
    for val in notDuplicationKeyList:
        tmpList = [index for index in range(len(keyList)) if keyList[index] == val]
        if len(tmpList) == 1:
            tmpCommKeyDict.update(**totalDictInsertList[tmpList[0]])
        else:
            tmpMulKeyDict.update({val:tmpList})

    if len(tmpMulKeyDict) == 0 :
        pass
        tmpCommKeyDict = handleStringJson(tmpCommKeyDict) #需要处理字典value的值是string类型，string的内容是json ，解析json
        totalList.append(tmpCommKeyDict)

    elif len(tmpMulKeyDict) == 1 :
        for k,v in tmpMulKeyDict.items():
            tmpCommKeyDict.update(**totalDictInsertList[v[0]])
            totalList.append(tmpCommKeyDict)
    else:
        for key, val in tmpMulKeyDict.items():
            num =  len(val)
            if num > maxNum:
                maxNum = num
        for i in range(maxNum):
            tmpDict = {}
            for key,val in tmpMulKeyDict.items():
                try:
                    tmpDict.update(tmpCommKeyDict,**totalDictInsertList[val[i]])
                except Exception as e:
                    print("跳过：",e)
            totalList.append(tmpDict)
    return totalList

def getClassDetailsData(string):

    commDataDict = {}
    totalList = []
    date = datetime.datetime.now().strftime("%Y_%m")
    tableName = "ClassDetails"

    for val in string["o"]:
        if not isinstance(val["Value"], list):
            commDataDict.update({val["Name"]: val["Value"]})
    for val in string["o"]:
        if val["Name"] == "Data":
            for val in val["Value"]:
                # print("---------------------------->1", val)
                tmpList = handleDetailsKeyData(val,"insert")
                for valdict in tmpList:
                    totalList.append(dict(valdict, **commDataDict))

    # print("+++++++++++++++++++++++",totalList)
    insertList = handleJsonTosql(totalList,tableName,date,commDataDict)
    # insertList = handleJsonTosql(totalList,tableName,"date",commDataDict,string)
    # print(insertList)
    # return  insertList

def getClassDetailsUpdateOperation(string,operation = "update"):

    id = string["o2"]["_id"]
    tableName = "ClassDetails"
    totalList = []
    updateData = []
    commDataDict = {}
    tmpDict = {}
    date = datetime.datetime.now().strftime("%Y_%m")
    tmpDict.update({"id":id})

    for value in string["o"] :
        if value["Name"] == "$set":
            updateData = value["Value"]

    for val in updateData:
        if not isinstance(val["Value"], list):
            commDataDict.update({val["Name"]: val["Value"]})

    if len(updateData) == 0:
        return  dict()
    else:
        for val in updateData:
            tmpDict.update({"updateRowNum":val["Name"]})
            if not isinstance(val["Value"], list):
                commDataDict.update({val["Name"]: val["Value"]})
            else:
                for i in handleDetailsKeyData(val,operation):
                    print(i)
                    totalList.append(dict(dict(tmpDict,**i),**commDataDict))
            totalList += handleDetailsKeyData(val,operation)
        print("------------------------------------------------------")
        # print(totalList)
        handleJsonTosql(totalList,tableName,date)
        print("------------------------------------------------------")



str002={"ts":6951716447626199343,"v":2,"op":"u","ns":"hamster.ClassDetails_2021_04_02","o":[{"Name":"$v","Value":1},{"Name":"$set","Value":[{"Name":"Data.156","Value":[{"Name":"ActionTime","Value":1618572612},{"Name":"UserSettings","Value":0},{"Name":"parser","Value":"stage"},{"Name":"Excluded","Value":[]},{"Name":"AffectedUserNum","Value":7},{"Name":"AID","Value":891915},{"Name":"TargetUID","Value":0},{"Name":"SourceUID","Value":12588578},{"Name":"IdenNum","Value":3},{"Name":"Idens","Value":[[{"Name":"OnlineOnly","Value":1},{"Name":"Identity","Value":4}],[{"Name":"OnlineOnly","Value":1},{"Name":"Identity","Value":1}],[{"Name":"OnlineOnly","Value":1},{"Name":"Identity","Value":2}]]},{"Name":"Cmd","Value":67371585},{"Name":"Flags","Value":2},{"Name":"GroupID","Value":0},{"Name":"AffectedUsers","Value":[[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":9483350},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":0}],[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":12379930},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":1}],[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":12978134},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":0}],[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":13088046},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":0}],[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":13745692},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":0}],[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":20156512},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":0}],[{"Name":"StageTime","Value":1618572612},{"Name":"UID","Value":33716684},{"Name":"AllowEnterTime","Value":0},{"Name":"Settings","Value":0}]]},{"Name":"Operation","Value":0},{"Name":"ExcludedNum","Value":0}]},{"Name":"Data.157","Value":[{"Name":"OwnerUID","Value":12379930},{"Name":"ActionTime","Value":1618572612},{"Name":"SourceUID","Value":12588578},{"Name":"Color","Value":"ClassMode.0"},{"Name":"Cmd","Value":67502162},{"Name":"parser","Value":"screenchange"},{"Name":"Stamp","Value":0},{"Name":"AID","Value":891917},{"Name":"TargetUID","Value":0}]},{"Name":"Data.158","Value":[{"Name":"bSend","Value":"False"},{"Name":"ActionTime","Value":1618572612},{"Name":"SourceUID","Value":0},{"Name":"BoundUID","Value":16450400},{"Name":"Color","Value":"hands up16450400"},{"Name":"Cmd","Value":67502160},{"Name":"Stamp","Value":0},{"Name":"AID","Value":891919},{"Name":"TargetUID","Value":0},{"Name":"GroupID","Value":0}]}]}],"o2":{"_id":"60797100693470eb1330210a"},"lsid":{"id":{"Kind":4,"Data":"EAAkU4lvQ4Wlle1uiUOZfg=="},"uid":"47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="},"txnNumber":98961}
# from test import xxx
# getClassDetailsData(xxx)
# getClassDetailsData(str002)
# getClassDetailsUpdateOperation(str002)

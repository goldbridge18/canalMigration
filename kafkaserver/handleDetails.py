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
            #print(handleDetailsKeyData(val,"update"))
            if not isinstance(val["Value"], list):
                commDataDict.update({val["Name"]: val["Value"]})
            else:
                for i in handleDetailsKeyData(val,operation):
                    totalList.append(dict(dict(tmpDict,**i),**commDataDict))
            totalList += handleDetailsKeyData(val,operation)
        #print("------------------------------------------------------")
        handleJsonTosql(totalList,tableName,date)
        #print("------------------------------------------------------")



str002= {'ts': 6953860916207157391, 'v': 2, 'op': 'u', 'ns': 'hamster.ClassDetails_2021_04_02', 'o': [{'Name': '$v', 'Value': 1}, {'Name': '$set', 'Value': [{'Name': 'Data.853', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071909}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26177532}, {'Name': 'Color', 'Value': 'webcamPositionGlobal'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'Mode', 'Value': 1}, {'Name': 'AID', 'Value': 166375}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}]}, {'Name': 'Data.854', 'Value': [{'Name': 'ActionTime', 'Value': 1619071909}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 1279}, {'Name': 'X1', 'Value': 640}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26286558}, {'Name': 'Color', 'Value': 'webcamPosition26286558'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 70}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166379}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.855', 'Value': [{'Name': 'ActionTime', 'Value': 1619071909}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 639}, {'Name': 'X1', 'Value': 0}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26531032}, {'Name': 'Color', 'Value': 'webcamPosition26531032'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 71}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166381}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.856', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071909}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 0}, {'Name': 'X2', 'Value': 0}, {'Name': 'X1', 'Value': 0}, {'Name': 'Y2', 'Value': 0}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26292426}, {'Name': 'Color', 'Value': 'webcamPosition26292426'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 1}, {'Name': 'ZIndex', 'Value': 69}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166383}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.857', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071909}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 639}, {'Name': 'X1', 'Value': 0}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26531032}, {'Name': 'Color', 'Value': 'webcamPosition26531032'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 71}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166385}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.858', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071909}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 1279}, {'Name': 'X1', 'Value': 640}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26286558}, {'Name': 'Color', 'Value': 'webcamPosition26286558'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 70}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166387}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.859', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26177532}, {'Name': 'Color', 'Value': 'webcamPositionGlobal'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'Mode', 'Value': 1}, {'Name': 'AID', 'Value': 166389}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}]}, {'Name': 'Data.860', 'Value': [{'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 1279}, {'Name': 'X1', 'Value': 852}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26286558}, {'Name': 'Color', 'Value': 'webcamPosition26286558'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 70}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166393}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.861', 'Value': [{'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 851}, {'Name': 'X1', 'Value': 426}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26531032}, {'Name': 'Color', 'Value': 'webcamPosition26531032'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 71}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166395}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.862', 'Value': [{'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 425}, {'Name': 'X1', 'Value': 0}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26292426}, {'Name': 'Color', 'Value': 'webcamPosition26292426'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 72}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166397}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.863', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 425}, {'Name': 'X1', 'Value': 0}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26292426}, {'Name': 'Color', 'Value': 'webcamPosition26292426'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 72}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166399}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.864', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 851}, {'Name': 'X1', 'Value': 426}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26531032}, {'Name': 'Color', 'Value': 'webcamPosition26531032'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 71}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166401}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}, {'Name': 'Data.865', 'Value': [{'Name': 'bSend', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619071910}, {'Name': 'Area', 'Value': [{'Name': 'Y1', 'Value': 130}, {'Name': 'X2', 'Value': 1279}, {'Name': 'X1', 'Value': 852}, {'Name': 'Y2', 'Value': 718}]}, {'Name': 'SourceUID', 'Value': 26177532}, {'Name': 'BoundUID', 'Value': 26286558}, {'Name': 'Color', 'Value': 'webcamPosition26286558'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'OnTop', 'Value': 0}, {'Name': 'ZIndex', 'Value': 70}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 166403}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}, {'Name': 'Channel', 'Value': 0}]}]}], 'o2': {'_id': '608107b2693470eb13a96608'}, 'lsid': {'id': {'Kind': 4, 'Data': 'Y9wacXSTTzGURWXokgtabg=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 205565}

str002 = {'ts': 6953892016065347784, 'v': 2, 'op': 'u', 'ns': 'hamster.ClassDetails_2021_04_06', 'o': [{'Name': '$v', 'Value': 1}, {'Name': '$set', 'Value': [{'Name': 'CloseTime', 'Value': 1619081586}, {'Name': 'Data.72', 'Value': [{'Name': 'FullScreen', 'Value': 0}, {'Name': 'ActionTime', 'Value': 1619079151}, {'Name': 'SourceUID', 'Value': 33629554}, {'Name': 'BoundUID', 'Value': 0}, {'Name': 'Color', 'Value': 'shareWidgetglobalData'}, {'Name': 'Cmd', 'Value': 67502160}, {'Name': 'MiniMized', 'Value': 0}, {'Name': 'Stamp', 'Value': 0}, {'Name': 'AID', 'Value': 315347}, {'Name': 'TargetUID', 'Value': 0}, {'Name': 'GroupID', 'Value': 0}]}]}], 'o2': {'_id': '608122c2693470eb134199ca'}, 'lsid': {'id': {'Kind': 4, 'Data': 'CLL9t1ZaTUO/OM/rVMLHbw=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 35848}

# from test import xxx
# getClassDetailsData(xxx)
# getClassDetailsData(str002)
getClassDetailsUpdateOperation(str002)

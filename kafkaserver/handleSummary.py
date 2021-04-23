# -*- coding:utf-8 -*-
import json
from collections  import abc
from kafkaserver.commServer import  handleJsonTosql
'''
处理 mongodb-shake工具从mongodb中抽进 kafka的json 数据
'''
def getKeyInDetailsData(string):
    totalList = []
    totalDict = {}
    commdict = {}
    tmpList = []
    # print(string)
    try:
        notListData = [v for x in string if not isinstance(x["Value"], abc.Sequence) for k, v in x.items()]
    except Exception as e:
        print("notListData is error !,可能是string里没有list类型的数据", e)
        print("error statment------>:", string)
        notListData = []

    if len(notListData) == 0:
        pass

    else:
        num = [x for x in range(len(notListData)) if x % 2 == 0]
        for i in num:
            commdict[notListData[i]] = notListData[i + 1]
    # print("---------comm--------",commdict)

    try:
        listData = [v for x in string if isinstance(x["Value"], abc.Sequence) for k, v in x.items()]
        if len(listData) == 0:
            totalList.append(commdict)
            return totalList
        else:
            detailsData = listData[1]
            num = [x for x in range(len(listData)) if x % 2 == 0]
            for i in num:
                tmpList.append({listData[i]: listData[i + 1]})

    except Exception as e:
        print("listData is error !", string)
        print("error statment------>:", string)
        tmpDict = {}
        if isinstance(string[0],list):

            for val in string[0]:
                tmpDict.update({val["Name"]:val["Value"]})
            return [dict(commdict,**tmpDict)]
        else:
            if len(string) == 0:
                string = ""
            else:
                string = str(string).replace("[","\"").replace("]","\"")
            if len(commdict) != 0:
                return totalList.append(commdict)
            else:
                return string

    for val in [v for x in tmpList for k, v in x.items()]:
        if listData[0] == "Details":
            for i in [x for x in range(len(val)) if x % 2 == 0]:
                tmp_list = []
                tmpDict = {}

                for value in detailsData[i]:
                    if value["Value"] == "In":
                        pass
                    else:
                        tmpDict[value["Name"] + "_in"] = value["Value"]
                try:
                    for value in detailsData[i + 1]:
                        if value["Value"] == "Out":
                            pass
                        else:
                            tmpDict[value["Name"] + "_out"] = value["Value"]
                except Exception as e:
                    print(e)
                # tmp_list.append(dict(tmpDict, **commdict))
                tmp_list.append(dict(tmpDict, **commdict))
                # totalList.append(tmp_list)
                totalList.append(dict(tmpDict, **commdict))

        elif listData[0] == "Camera":
            if isinstance(listData[1], abc.Sequence):
                tmpList = [z for x in tmpList for k, v in x.items() for y, z in v[0].items()]
                num = [x for x in range(len(tmpList)) if x % 2 == 0]
                for i in num:
                    commdict[tmpList[i]] = tmpList[i + 1]
                totalList.append(commdict)
                return totalList
        else:
            pass

    return totalList


def getinoutEndData(string):
    keyName = string["Name"]
    totalList = []
    commdict={}
    # print(string)
    notListData = [v for x in string["Value"] if not isinstance(x["Value"],abc.Sequence) for k,v in x.items()]
    num = [x for x in range(len(notListData)) if x%2 ==0]
    for i in num:
        commdict[notListData[i]] = notListData[i + 1]
    listData = [v for x in string["Value"] if isinstance(x["Value"],abc.Sequence) for k,v in x.items()]
    if len(listData) == 0:
        totalList.append(commdict)
    else:
        num1 = [x for x in range(len(listData)) if x%2 ==0]
        tmpdict = {}
        for i in num1:
            tmpdict[listData[i]] = listData[i + 1]

        for key ,val in tmpdict.items():
            if len(val) == 0:
                totalList.append(dict({key: ""},**commdict))
            else:
                pass
                totalList.append(dict({key: getKeyInDetailsData(val)},**commdict))
    # print(totalList)
    return totalList

def getGroupingData(groupLists1):
    groupLists = groupLists1["Value"][0]["Value"]
    tmpdict = {}
    totalList = []
    try:
        #json 同一层数据 key为Items
        itemsData = [x for x in groupLists if x["Name"] == "Items"][0]
        notItemsData = [v for x in groupLists if x["Name"] != "Items" for k,v in x.items()]

        num = [x for x in range(len(notItemsData)) if x%2 ==0]

        for i in  num:
            if notItemsData[i] == "Duration": #Duration 的key 和子层下面的 key冲突
                tmpdict["groupEnd_{xxx}".format(xxx = notItemsData[i])] = notItemsData[i + 1]
            else:
                tmpdict[notItemsData[i]] = notItemsData[i + 1]

        #json 同一层数据 Groups
        for value in itemsData["Value"]:
            groupsData = [x for x in value if x["Name"] == "Groups"][0]
            notGroupsData = [v for x in value if x["Name"] != "Groups" for k,v in x.items()]
            num1 = [x for x in range(len(notGroupsData)) if x%2 ==0]

            for i in  num1:
                tmpdict[notGroupsData[i]] = notGroupsData[i + 1]

            #处理 Groups数据
            if isinstance(groupsData["Value"], abc.Sequence):
                for val in groupsData["Value"]:

                    for val01 in val:
                        if isinstance(val01["Value"], abc.Sequence):
                            tmpdict.update({"Groups": val01["Name"]})
                            groupMemberList = []
                            for val02 in val01["Value"]:
                                tmpList = [{x["Name"]: x["Value"]} for x in val02]
                                # groupMemberList.append(
                                #     dict(dict(tmpList[0], **tmpList[1]), **dict(tmpdict)))
                                totalList.append(dict(dict(tmpList[0], **tmpList[1]), **dict(tmpdict)))
                            # totalList.append(groupMemberList)
                            # totalList.append(dict(dict(tmpList[0], **tmpList[1]), **dict(tmpdict)))
            else:
                pass
    except Exception as e:
        print(e)
    return totalList

def getFilesData(string):
    totalList = []
    commdict={}
    try:
        notListData = [v for x in string["Value"] if not isinstance(x["Value"],abc.Sequence) for k,v in x.items()]
        num = [x for x in range(len(notListData)) if x%2 ==0]
        for i in num:
            commdict[notListData[i]] = notListData[i + 1]

        listData = [v for x in string["Value"] if isinstance(x["Value"],abc.Sequence) for k,v in x.items()]
        num1 = [x for x in range(len(listData)) if x%2 ==0]
        for i in num1:
            tmpdict ={}
            tmpdict[listData[i]] = listData[i + 1]

        for key,val in tmpdict.items():
            tmpdict01 ={}
            tmpdict02 ={}
            for val01 in val:
                data = [v for x in val01 for k,v in x.items()]
                num = [x for x in range(len(data)) if x%2 ==0]
                for i in num:
                    tmpdict01[data[i]] = data[i + 1]
                tmpdict02= dict(tmpdict01,**commdict)
                totalList.append(tmpdict02)
    except Exception as e:
        print("getFilesData",e)
    return totalList


def getPersonsdata(string):
    tmpDict = {}

    totalDict = {}
    totalList = []
    commdict = {}
    tmpdict = {}
    notListData = [v for x in string["Value"] if not isinstance(x["Value"], abc.Sequence) for k, v in x.items()]
    num = [x for x in range(len(notListData)) if x % 2 == 0]
    for i in num:
        commdict[notListData[i]] = notListData[i + 1]

    listData = [v for x in string["Value"] if isinstance(x["Value"], abc.Sequence) for k, v in x.items()]
    # print("-------------->", listData)
    if len(listData) == 0:
        totalList.append(commdict)
    else:
        num1 = [x for x in range(len(listData)) if x % 2 == 0]

        for i in num1:
            tmpdict[listData[i]] = listData[i + 1]

    # 'Name': 'xxx', 'Value': [{'Name': 'SilenceAll', 'Value': [xxxxx}}, {'Name': 'Persons', 'Value': [xxxx]}]}
    # key为多个list值，SilenceAll的值是Persons里的每个list共同需要的值。 因此：先提出公共部分
    for keyName in tmpdict:
        if keyName == "SilenceAll":
            valList = [v for x in tmpdict[keyName] for k, v in x.items()]
            num = [x for x in range(len(valList)) if x % 2 == 0]
            # print("-----------valList-------", valList)
            for i in num:
                tmpDict["SilenceAll_{xx}".format(xx=valList[i])] = valList[i + 1]

        elif keyName == "MuteAll":
            valList =  [ v for x in tmpdict[keyName] for k,v in x.items()]
            num = [x for x in range(len(valList)) if x % 2 == 0]
            for i in num:
                tmpList = []
                if valList[i] == "Total":
                    tmpDict["MuteAll_{xx}".format(xx=valList[i])] = valList[i + 1]
                else:
                    tmpDict[valList[i]] = valList[i + 1]
            #     tmpList.append(dict(tmpDict, **commdict))
            # totalList.append({valList[i]: tmpList})

    for keyName in tmpdict:
        if keyName in ["Persons"]:
            valList = [v for x in tmpdict[keyName] for k, v in x.items()]
            num = [x for x in range(len(valList)) if x % 2 == 0]
            for i in num:
                tmpList = []
                valList01 = [v for x in valList[i + 1] for k,v in x.items()]
                num01 = [x for x in range(len(valList01)) if x % 2 == 0]
                for i01 in num01:
                    # totalDict[valList[i]] = dict({"Persons_{xx}".format(xx=valList01[i01]):valList01[i01 + 1]},**tmpDict)
                    tmpDict["Persons_{xx}".format(xx=valList01[i01])] = valList01[i01 + 1]
                    tmpList.append(dict(tmpDict,**commdict))
                totalList.append({valList[i]:tmpList})
                    # totalDict[valList[i]] = dict({"Persons_{xx}".format(xx=valList01[i01]):valList01[i01 + 1]},**tmpDict)
    return totalList


def handlAnswersChildrendata(string):

    totalList = []
    for val in string:

        commdict = {}
        tmpdict= {}
        tmpListToDict = {}

        try:
            notListData = [v for x in val if not isinstance(x["Value"], list) for k, v in x.items()]
        except Exception as e:
            print(e)

        num = [x for x in range(len(notListData)) if x % 2 == 0]
        for i in num:
            commdict[notListData[i]] = notListData[i + 1]

        listData = [v for x in val if isinstance(x["Value"], list) and len(x["Value"]) != 0 for k, v in
                    x.items()]
        if len(listData) == 0:
            totalList.append(commdict)
            return totalList
        else:
            num1 = [x for x in range(len(listData)) if x % 2 == 0]

            for i in num1:
                tmpdict[listData[i]] = listData[i + 1]
        # print(tmpdict)
        tmpDictDataList = []
        keyIsNumDict = {}
        for key in tmpdict:

            if len(tmpdict[key]) > 0 and isinstance(tmpdict[key][0],list) and not key.isdigit():
                for tmpDictInList in  tmpdict[key]:
                    tmpDictInLisData = [v for x in tmpDictInList  for k,v in x.items()]
                    num2 = [x for x in range(len(tmpDictInLisData)) if x % 2 == 0]

                    for i in num2:
                        tmpListToDict[tmpDictInLisData[i]] = tmpDictInLisData[i + 1]
                    tmpDictDataList.append(dict(tmpListToDict,**commdict))
            elif key.isdigit():

                tmpDictInLisData = [v for x in tmpdict[key] for k, v in x.items()]
                num2 = [x for x in range(len(tmpDictInLisData)) if x % 2 == 0]
                tmpKeyIsNumDict = {}
                for i in num2:
                    tmpKeyIsNumDict[tmpDictInLisData[i]] = tmpDictInLisData[i + 1]
                keyIsNumDict[key] = tmpKeyIsNumDict
            else:
                tmpDictInLisData = [v for x in tmpdict[key]  for k, v in x.items()]
                num2 = [x for x in range(len(tmpDictInLisData)) if x % 2 == 0]
                for i in num2:
                    tmpListToDict[tmpDictInLisData[i]] = tmpDictInLisData[i + 1]

        for key,value in keyIsNumDict.items():

            for listData01 in tmpDictDataList:
                if listData01["Uid"] == int(key):
                    indexNum = tmpDictDataList.index(listData01) #获取下表 更新list的值
                    tmpDictDataList[indexNum] = dict(listData01, **value)
        # print("===========",tmpDictDataList

        totalList = tmpDictDataList
    return totalList

def getAnswersdata(string):

    totalList = []
    commdict = {}
    tmpdict = {}
    notListData = [v for x in string["Value"] if not isinstance(x["Value"], abc.Sequence)  for k, v in x.items()]
    num = [x for x in range(len(notListData)) if x % 2 == 0]
    for i in num:
        commdict[notListData[i]] = notListData[i + 1]

    listData = [v for x in string["Value"] if isinstance(x["Value"], abc.Sequence) and len(x["Value"]) != 0 for k, v in x.items()]
    # print("-------------->2", listData)
    if len(listData) == 0:
        totalList.append(commdict)
        return totalList
    else:
        num1 = [x for x in range(len(listData)) if x % 2 == 0]

        for i in num1:
            tmpdict[listData[i]] = listData[i + 1]
    tmpList = handlAnswersChildrendata(tmpdict["Answers"])  #调用函数 handlAnswersChildrendata

    # totalList = [dict(y,**commdict) for x in  tmpList for y in x]
    totalList = [dict(x, **commdict) for x in tmpList]
    return  totalList


#获取summary数据
def getClassSummaryNum(dict_data):
    commDataDict = {}
    detailDataDict = {}
    sqlStatement = []
    datas = []
    tableName = "classsummary"
    for val in dict_data["o"]:
        if not isinstance(val["Value"],list):
            commDataDict.update({val["Name"]: val["Value"]})
    # print("---------comm----------->",commDataDict)
    for val in dict_data["o"]:
        if val["Name"] == "Data":
            for i in val["Value"]:

                if i["Name"] == "groupEnd":
                    datas = getGroupingData(i)
                    # print("------------------->",datas)
                    handleJsonTosql(datas, tableName,i["Name"],commDataDict)
                elif i["Name"] in ["sharewidgetEnd", "edbEnd","responderEnd"]:
                    datas = getFilesData(i)
                    # print("------------------->", datas)
                    handleJsonTosql(datas, tableName,i["Name"],commDataDict)
                    # detailDataDict.update({"sharewidgetEnd":getFilesData(i)})
                elif i["Name"] in ["inoutEnd" , "authorizeEnd" ,"awardEnd" , "stageEnd" , "handsupEnd" ,
                                   "textboardEnd","screenshareEnd","equipmentsEnd",'mdscreenEnd','diceEnd','timerEnd', 'kickoutEnd','randomselEnd',
                                   'smallboardEnd',"teachingcameraEnd"]:
                    datas = getinoutEndData(i)
                    # print("------------------->", datas)
                    handleJsonTosql(datas,tableName, i["Name"],commDataDict)
                    # detailDataDict.update({"inoutEnd":getinoutEndData(i)})
                elif i["Name"] in ["answerEnd"]:
                    datas = getAnswersdata(i)
                    # print("------------------->", datas)
                    handleJsonTosql(datas,tableName, i["Name"],commDataDict)
                elif i["Name"] in ["muteEnd" ,"silenceEnd"]:
                    datas = getPersonsdata(i)
                    # print("------------->",datas)
                    handleJsonTosql(datas,tableName, i["Name"],commDataDict)
                else:
                    print("--------+++++++++++++---------",i)
                    from common.loggerout  import writeLogContext
                    writeLogContext(i, "info")
                    # print(getDataToCover(i))
                    # detailDataDict.update(getDataToCover(i))
        else:
            # commDataDict.update({val["Name"]:val["Value"]})
            pass


#str002={"ts":6932296697162760587,"v":2,"op":"i","ns":"hamster.ClassSummary49","o":[{"Name":"_id","Value":"6034771e433a0974dad41b07"},{"Name":"ActionTime","Value":1614051102},{"Name":"CID","Value":288958577},{"Name":"CourseID","Value":136446085},{"Name":"Cmd","Value":"End"},{"Name":"CloseTime","Value":1614051011},{"Name":"StartTime","Value":1614048551},{"Name":"SID","Value":26323998},{"Name":"Data","Value":[{"Name":"teachingcameraEnd","Value":[{"Name":"Total","Value":24},{"Name":"Details","Value":[{"Name":"Video","Value":0},{"Name":"Net","Value":24},{"Name":"Local","Value":0}]},{"Name":"Times","Value":1}]}]}],"o2":"","lsid":{"id":{"Kind":4,"Data":"BoJQTGeTTjSBDXxRIF/YlA=="},"uid":"47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="},"txnNumber":784900}
# getClassSummaryNum(str002)
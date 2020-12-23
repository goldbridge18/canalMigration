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
                                   'smallboardEnd']:
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




# from kafkaserver.handleDetails import handleDetailsKeyData
#
# str002 = {'ts': 6872270994443075586, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary46', 'o': [{'Name': '_id', 'Value': '5f5f364c3c5f770855b4e8ef'}, {'Name': 'ActionTime', 'Value': 1600075340}, {'Name': 'CID', 'Value': 396928}, {'Name': 'CourseID', 'Value': 148163}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1600075250}, {'Name': 'StartTime', 'Value': 1600050650}, {'Name': 'SID', 'Value': 1012192}, {'Name': 'Data', 'Value': [{'Name': 'stageEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'UpTotal', 'Value': 40}, {'Name': 'DownCount', 'Value': 8}, {'Name': 'UpCount', 'Value': 6}, {'Name': 'DownTotal', 'Value': 6729}]}, {'Name': '1012192', 'Value': [{'Name': 'UpTotal', 'Value': 22432}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 21}, {'Name': 'DownTotal', 'Value': 0}]}, {'Name': '1012194', 'Value': [{'Name': 'UpTotal', 'Value': 2793}, {'Name': 'DownCount', 'Value': 20}, {'Name': 'UpCount', 'Value': 11}, {'Name': 'DownTotal', 'Value': 14998}]}, {'Name': '1015198', 'Value': [{'Name': 'UpTotal', 'Value': 0}, {'Name': 'DownCount', 'Value': 1}, {'Name': 'UpCount', 'Value': 0}, {'Name': 'DownTotal', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'UpTotal', 'Value': 0}, {'Name': 'DownCount', 'Value': 5}, {'Name': 'UpCount', 'Value': 0}, {'Name': 'DownTotal', 'Value': 16713}]}]}, {'Name': 'handsupEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'CTime', 'Value': 158}, {'Name': 'Total', 'Value': 9}]}]}, {'Name': 'sharewidgetEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'EndTime', 'Value': 1600066442}, {'Name': 'FileId', 'Value': '43944-1012192'}, {'Name': 'Type', 'Value': 8}, {'Name': 'StartTime', 'Value': 1600066426}, {'Name': 'FileName', 'Value': '测试专用（不使用 classin 授权规则）.edu'}], [{'Name': 'EndTime', 'Value': 1600069770}, {'Name': 'FileId', 'Value': '42879-1012192'}, {'Name': 'Type', 'Value': 3}, {'Name': 'StartTime', 'Value': 1600066294}, {'Name': 'FileName', 'Value': '贝贝.mp3'}], [{'Name': 'EndTime', 'Value': 1600069908}, {'Name': 'FileId', 'Value': '42882-1012192'}, {'Name': 'Type', 'Value': 1}, {'Name': 'StartTime', 'Value': 1600064819}, {'Name': 'FileName', 'Value': 'Best 2nd - 副本 - 副本 - 副本 (2) - 副本.pptx'}], [{'Name': 'EndTime', 'Value': 1600073616}, {'Name': 'FileId', 'Value': '44063-1012192'}, {'Name': 'Type', 'Value': 6}, {'Name': 'StartTime', 'Value': 1600072626}, {'Name': 'FileName', 'Value': '数独.eda'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '42881-1012192'}, {'Name': 'Type', 'Value': 4}, {'Name': 'StartTime', 'Value': 1600064746}, {'Name': 'FileName', 'Value': '直线与椭圆的副本 - 副本 - 副本 - 副本 - 副本 (3).pdf'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43890-1012192'}, {'Name': 'Type', 'Value': 1}, {'Name': 'StartTime', 'Value': 1600071707}, {'Name': 'FileName', 'Value': 'moreaction.pptx'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '46690-1012192'}, {'Name': 'Type', 'Value': 3}, {'Name': 'StartTime', 'Value': 1600066357}, {'Name': 'FileName', 'Value': '我和我的祖国_new.flac'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43891-1012192'}, {'Name': 'Type', 'Value': 2}, {'Name': 'StartTime', 'Value': 1600072071}, {'Name': 'FileName', 'Value': '2平方与开平方.mp4'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43889-1012192'}, {'Name': 'Type', 'Value': 4}, {'Name': 'StartTime', 'Value': 1600069214}, {'Name': 'FileName', 'Value': '2020.5作业迭代八.pdf'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43885-1012192'}, {'Name': 'Type', 'Value': 3}, {'Name': 'StartTime', 'Value': 1600069766}, {'Name': 'FileName', 'Value': '不才 - 化身孤岛的鲸_new.wav'}]]}, {'Name': 'Count', 'Value': 10}, {'Name': 'Total', 'Value': 47210}]}, {'Name': 'awardEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 10}]}]}, {'Name': 'textboardEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 928}, {'Name': 'Period', 'Value': [928]}, {'Name': 'DCount', 'Value': 1}]}, {'Name': 'inoutEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600067672}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600069288}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600069288}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600074441}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600050873}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051015}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051016}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051026}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051027}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052188}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052189}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052205}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052205}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053722}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053722}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053737}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053738}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053748}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053748}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053758}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053759}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053812}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053813}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053831}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053831}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600063017}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600063017}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600063493}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600063493}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600063679}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600063679}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600064075}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600064076}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067210}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600067702}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067826}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600068025}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600068712}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600068712}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600072650}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600072963}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600072995}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600073029}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600073068}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600073121}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600074403}]]}, {'Name': 'Identity', 'Value': 3}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051045}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051061}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051061}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051073}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051073}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052148}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052153}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052166}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052167}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052176}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052176}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600058762}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600064171}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600069339}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600069339}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600071750}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600071837}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600074429}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600054066}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600054159}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600050896}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051274}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051275}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053303}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053304}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600066953}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600066983}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067008}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600067008}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067641}]]}, {'Name': 'Identity', 'Value': 4}]}]}, {'Name': 'authorizeEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012192', 'Value': [{'Name': 'Count', 'Value': 21}, {'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 4}]}, {'Name': '1015198', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012329', 'Value': [{'Name': 'Count', 'Value': 5}, {'Name': 'Total', 'Value': 16713}]}]}, {'Name': 'groupEnd', 'Value': [{'Name': 'Grouping', 'Value': [{'Name': 'Count', 'Value': 2}, {'Name': 'Items', 'Value': [[{'Name': 'Duration', 'Value': 196}, {'Name': 'Groups', 'Value': [[{'Name': '1', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012193}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012194}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012198}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1015198}]]}], [{'Name': '2', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012196}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012197}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012199}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012200}]]}]]}, {'Name': 'StartTime', 'Value': 1600053074}], [{'Name': 'Duration', 'Value': 102}, {'Name': 'Groups', 'Value': [[{'Name': '1', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012193}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012194}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012197}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012199}]]}], [{'Name': '2', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012196}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012198}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012200}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1015198}]]}]]}, {'Name': 'StartTime', 'Value': 1600053614}]]}, {'Name': 'Duration', 'Value': 298}]}]}, {'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': [38]}]}, {'Name': 'edbEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'FileKey', 'Value': '47001-1012192'}, {'Name': 'ActionTime', 'Value': 1600066453}, {'Name': 'FileSource', 'Value': 1}, {'Name': 'FileName', 'Value': '小微测试20 - 118_20200912_141039.edb'}]]}]}, {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}]}]}, {'Name': 'MuteAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}]}, {'Name': 'silenceEnd', 'Value': [{'Name': 'SilenceAll', 'Value': [{'Name': 'Count', 'Value': 4}, {'Name': 'Total', 'Value': 26}]}, {'Name': 'Persons', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}]}]}]}, {'Name': 'equipmentsEnd', 'Value': [{'Name': '1012329', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012193', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012192', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1282}]}]}, {'Name': '1015198', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012194', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'yWIb71VOSnq6nnqauwVczw=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 7637}
# str002 = {'ts': 6872270994443075586, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary46', 'o': [{'Name': '_id', 'Value': '5f5f364c3c5f770855b4e8ef'}, {'Name': 'ActionTime', 'Value': 1600075340}, {'Name': 'CID', 'Value': 396928}, {'Name': 'CourseID', 'Value': 148163}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1600075250}, {'Name': 'StartTime', 'Value': 1600050650}, {'Name': 'SID', 'Value': 1012192}, {'Name': 'Data', 'Value': [{'Name': 'stageEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'UpTotal', 'Value': 40}, {'Name': 'DownCount', 'Value': 8}, {'Name': 'UpCount', 'Value': 6}, {'Name': 'DownTotal', 'Value': 6729}]}, {'Name': '1012192', 'Value': [{'Name': 'UpTotal', 'Value': 22432}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 21}, {'Name': 'DownTotal', 'Value': 0}]}, {'Name': '1012194', 'Value': [{'Name': 'UpTotal', 'Value': 2793}, {'Name': 'DownCount', 'Value': 20}, {'Name': 'UpCount', 'Value': 11}, {'Name': 'DownTotal', 'Value': 14998}]}, {'Name': '1015198', 'Value': [{'Name': 'UpTotal', 'Value': 0}, {'Name': 'DownCount', 'Value': 1}, {'Name': 'UpCount', 'Value': 0}, {'Name': 'DownTotal', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'UpTotal', 'Value': 0}, {'Name': 'DownCount', 'Value': 5}, {'Name': 'UpCount', 'Value': 0}, {'Name': 'DownTotal', 'Value': 16713}]}]}, {'Name': 'handsupEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'CTime', 'Value': 158}, {'Name': 'Total', 'Value': 9}]}]}, {'Name': 'sharewidgetEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'EndTime', 'Value': 1600066442}, {'Name': 'FileId', 'Value': '43944-1012192'}, {'Name': 'Type', 'Value': 8}, {'Name': 'StartTime', 'Value': 1600066426}, {'Name': 'FileName', 'Value': '测试专用（不使用 classin 授权规则）.edu'}], [{'Name': 'EndTime', 'Value': 1600069770}, {'Name': 'FileId', 'Value': '42879-1012192'}, {'Name': 'Type', 'Value': 3}, {'Name': 'StartTime', 'Value': 1600066294}, {'Name': 'FileName', 'Value': '贝贝.mp3'}], [{'Name': 'EndTime', 'Value': 1600069908}, {'Name': 'FileId', 'Value': '42882-1012192'}, {'Name': 'Type', 'Value': 1}, {'Name': 'StartTime', 'Value': 1600064819}, {'Name': 'FileName', 'Value': 'Best 2nd - 副本 - 副本 - 副本 (2) - 副本.pptx'}], [{'Name': 'EndTime', 'Value': 1600073616}, {'Name': 'FileId', 'Value': '44063-1012192'}, {'Name': 'Type', 'Value': 6}, {'Name': 'StartTime', 'Value': 1600072626}, {'Name': 'FileName', 'Value': '数独.eda'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '42881-1012192'}, {'Name': 'Type', 'Value': 4}, {'Name': 'StartTime', 'Value': 1600064746}, {'Name': 'FileName', 'Value': '直线与椭圆的副本 - 副本 - 副本 - 副本 - 副本 (3).pdf'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43890-1012192'}, {'Name': 'Type', 'Value': 1}, {'Name': 'StartTime', 'Value': 1600071707}, {'Name': 'FileName', 'Value': 'moreaction.pptx'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '46690-1012192'}, {'Name': 'Type', 'Value': 3}, {'Name': 'StartTime', 'Value': 1600066357}, {'Name': 'FileName', 'Value': '我和我的祖国_new.flac'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43891-1012192'}, {'Name': 'Type', 'Value': 2}, {'Name': 'StartTime', 'Value': 1600072071}, {'Name': 'FileName', 'Value': '2平方与开平方.mp4'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43889-1012192'}, {'Name': 'Type', 'Value': 4}, {'Name': 'StartTime', 'Value': 1600069214}, {'Name': 'FileName', 'Value': '2020.5作业迭代八.pdf'}], [{'Name': 'EndTime', 'Value': 1600075250}, {'Name': 'FileId', 'Value': '43885-1012192'}, {'Name': 'Type', 'Value': 3}, {'Name': 'StartTime', 'Value': 1600069766}, {'Name': 'FileName', 'Value': '不才 - 化身孤岛的鲸_new.wav'}]]}, {'Name': 'Count', 'Value': 10}, {'Name': 'Total', 'Value': 47210}]}, {'Name': 'awardEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 10}]}]}, {'Name': 'textboardEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 928}, {'Name': 'Period', 'Value': [928,1000]}, {'Name': 'DCount', 'Value': 1}]}, {'Name': 'inoutEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600067672}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600069288}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600069288}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600074441}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600050873}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051015}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051016}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051026}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051027}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052188}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052189}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052205}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052205}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053722}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053722}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053737}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053738}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053748}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053748}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053758}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053759}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053812}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053813}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053831}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053831}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600063017}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600063017}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600063493}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600063493}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600063679}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600063679}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600064075}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600064076}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067210}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600067702}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067826}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600068025}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600068712}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600068712}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600072650}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600072963}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600072995}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600073029}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600073068}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600073121}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600074403}]]}, {'Name': 'Identity', 'Value': 3}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051045}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051061}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051061}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051073}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051073}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052148}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052153}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052166}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052167}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600052176}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600052176}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600058762}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600064171}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600069339}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600069339}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600071750}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600071837}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600074429}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600054066}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600054159}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600050896}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600051274}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600051275}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600053303}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600053304}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600066953}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600066983}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067008}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1600067008}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1600067641}]]}, {'Name': 'Identity', 'Value': 4}]}]}, {'Name': 'authorizeEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012192', 'Value': [{'Name': 'Count', 'Value': 21}, {'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 4}]}, {'Name': '1015198', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012329', 'Value': [{'Name': 'Count', 'Value': 5}, {'Name': 'Total', 'Value': 16713}]}]}, {'Name': 'groupEnd', 'Value': [{'Name': 'Grouping', 'Value': [{'Name': 'Count', 'Value': 2}, {'Name': 'Items', 'Value': [[{'Name': 'Duration', 'Value': 196}, {'Name': 'Groups', 'Value': [[{'Name': '1', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012193}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012194}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012198}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1015198}]]}], [{'Name': '2', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012196}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012197}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012199}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012200}]]}]]}, {'Name': 'StartTime', 'Value': 1600053074}], [{'Name': 'Duration', 'Value': 102}, {'Name': 'Groups', 'Value': [[{'Name': '1', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012193}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012194}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012197}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012199}]]}], [{'Name': '2', 'Value': [[{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012196}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1012198}], [{'Name': 'Role', 'Value': 1}, {'Name': 'UID', 'Value': 1012200}], [{'Name': 'Role', 'Value': 0}, {'Name': 'UID', 'Value': 1015198}]]}]]}, {'Name': 'StartTime', 'Value': 1600053614}]]}, {'Name': 'Duration', 'Value': 298}]}]}, {'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': [38]}]}, {'Name': 'edbEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'FileKey', 'Value': '47001-1012192'}, {'Name': 'ActionTime', 'Value': 1600066453}, {'Name': 'FileSource', 'Value': 1}, {'Name': 'FileName', 'Value': '小微测试20 - 118_20200912_141039.edb'}]]}]}, {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}]}]}, {'Name': 'MuteAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}]}, {'Name': 'silenceEnd', 'Value': [{'Name': 'SilenceAll', 'Value': [{'Name': 'Count', 'Value': 4}, {'Name': 'Total', 'Value': 26}]}, {'Name': 'Persons', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}]}]}]}, {'Name': 'equipmentsEnd', 'Value': [{'Name': '1012329', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012193', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012192', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1282}]}]}, {'Name': '1015198', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012194', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'yWIb71VOSnq6nnqauwVczw=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 7637}

# str002 = {'ts': 6872270994443075586, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary46', 'o': [{'Name': '_id', 'Value': '5f5f364c3c5f770855b4e8ef'}, {'Name': 'ActionTime', 'Value': 1600075340}, {'Name': 'CID', 'Value': 396928}, {'Name': 'CourseID', 'Value': 148163}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1600075250}, {'Name': 'StartTime', 'Value': 1600050650}, {'Name': 'SID', 'Value': 1012192}, {'Name': 'Data', 'Value': [ {'Name': 'handsupEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'CTime', 'Value': 158}, {'Name': 'Total', 'Value': 9}]}]},  {'Name': 'awardEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 10}]}]}, {'Name': 'textboardEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 928}, {'Name': 'Period', 'Value': [928,1000]}, {'Name': 'DCount', 'Value': 1}]}, {'Name': 'authorizeEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012192', 'Value': [{'Name': 'Count', 'Value': 21}, {'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 4}]}, {'Name': '1015198', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012329', 'Value': [{'Name': 'Count', 'Value': 5}, {'Name': 'Total', 'Value': 16713}]}]},  {'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': [38]}]}, {'Name': 'edbEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'FileKey', 'Value': '47001-1012192'}, {'Name': 'ActionTime', 'Value': 1600066453}, {'Name': 'FileSource', 'Value': 1}, {'Name': 'FileName', 'Value': '小微测试20 - 118_20200912_141039.edb'}]]}]}, {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}]}]}, {'Name': 'MuteAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}]}, {'Name': 'silenceEnd', 'Value': [{'Name': 'SilenceAll', 'Value': [{'Name': 'Count', 'Value': 4}, {'Name': 'Total', 'Value': 26}]}, {'Name': 'Persons', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Total', 'Value': 6769}]}, {'Name': '1012192', 'Value': [{'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 17882}]}, {'Name': '1015198', 'Value': [{'Name': 'Total', 'Value': 93}]}, {'Name': '1012329', 'Value': [{'Name': 'Total', 'Value': 16713}]}]}]}, {'Name': 'equipmentsEnd', 'Value': [{'Name': '1012329', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012193', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012192', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1282}]}]}, {'Name': '1015198', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}, {'Name': '1012194', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 0}]}]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'yWIb71VOSnq6nnqauwVczw=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 7637}
str002 = {'ts': 6872270994443075586, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary46', 'o': [{'Name': '_id', 'Value': '5f5f364c3c5f770855b4e8ef'}, {'Name': 'ActionTime', 'Value': 1600075340}, {'Name': 'CID', 'Value': 396928}, {'Name': 'CourseID', 'Value': 148163}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1600075250}, {'Name': 'StartTime', 'Value': 1600050650}, {'Name': 'SID', 'Value': 1012192}, {'Name': 'Data', 'Value': [ {'Name': 'handsupEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'CTime', 'Value': 158}, {'Name': 'Total', 'Value': 9}]}]},  {'Name': 'awardEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 10}]}]}, {'Name': 'textboardEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 928}, {'Name': 'Period', 'Value': [928,1000]}, {'Name': 'DCount', 'Value': 1}]}, {'Name': 'authorizeEnd', 'Value': [{'Name': '1012193', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012192', 'Value': [{'Name': 'Count', 'Value': 21}, {'Name': 'Total', 'Value': 22432}]}, {'Name': '1012194', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 4}]}, {'Name': '1015198', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1012329', 'Value': [{'Name': 'Count', 'Value': 5}, {'Name': 'Total', 'Value': 16713}]}]},  {'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': [38]}]}, {'Name': 'edbEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'FileKey', 'Value': '47001-1012192'}, {'Name': 'ActionTime', 'Value': 1600066453}, {'Name': 'FileSource', 'Value': 1}, {'Name': 'FileName', 'Value': '小微测试20 - 118_20200912_141039.edb'}]]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'yWIb71VOSnq6nnqauwVczw=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 7637}
str002 = {'ts': 6872270994443075586, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary46', 'o': [{'Name': '_id', 'Value': '5f5f364c3c5f770855b4e8ef'}, {'Name': 'ActionTime', 'Value': 1600075340}, {'Name': 'CID', 'Value': 396928}, {'Name': 'CourseID', 'Value': 148163}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1600075250}, {'Name': 'StartTime', 'Value': 1600050650}, {'Name': 'SID', 'Value': 1012192}, {'Name': 'Data', 'Value': [ {'Name': 'handsupEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'CTime', 'Value': 158}, {'Name': 'Total', 'Value': 9}]}]},  {'Name': 'awardEnd', 'Value': [{'Name': '1012194', 'Value': [{'Name': 'Total', 'Value': 10}]}]}, {'Name': 'textboardEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 928}, {'Name': 'Period', 'Value': [928,1000]}, {'Name': 'DCount', 'Value': 1}]}, {'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': [38]}]}, {'Name': 'edbEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'FileKey', 'Value': '47001-1012192'}, {'Name': 'ActionTime', 'Value': 1600066453}, {'Name': 'FileSource', 'Value': 1}, {'Name': 'FileName', 'Value': '小微测试20 - 118_20200912_141039.edb'}]]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'yWIb71VOSnq6nnqauwVczw=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 7637}
str002 = {'ts': 6908989279741935815, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary5', 'o': [{'Name': '_id', 'Value': '5fe1a925f3c5233407490799'}, {'Name': 'ActionTime', 'Value': 1608624421}, {'Name': 'CID', 'Value': 260605243}, {'Name': 'CourseID', 'Value': 121402475}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1608624331}, {'Name': 'StartTime', 'Value': 1608621600}, {'Name': 'SID', 'Value': 1153410}, {'Name': 'Data', 'Value': [{'Name': 'stageEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'UpTotal', 'Value': 1800}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 2}, {'Name': 'DownTotal', 'Value': 0}]}, {'Name': '1909074', 'Value': [{'Name': 'UpTotal', 'Value': 1575}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 1}, {'Name': 'DownTotal', 'Value': 0}]}]}, {'Name': 'handsupEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'CTime', 'Value': 3}, {'Name': 'Total', 'Value': 1}]}]}, {'Name': 'sharewidgetEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'EndTime', 'Value': 1608621835}, {'Name': 'FileId', 'Value': '192619485-1153410'}, {'Name': 'Type', 'Value': 2}, {'Name': 'StartTime', 'Value': 1608621696}, {'Name': 'FileName', 'Value': '589d8a8e441511eb8d8e00163e2eb842.mp4'}], [{'Name': 'EndTime', 'Value': 1608624300}, {'Name': 'FileId', 'Value': '192619495-1153410'}, {'Name': 'Type', 'Value': 1}, {'Name': 'StartTime', 'Value': 1608621629}, {'Name': 'FileName', 'Value': '6015819a441511eb97ae00163e2eb842.pptx'}]]}, {'Name': 'Count', 'Value': 2}, {'Name': 'Total', 'Value': 2810}]}, {'Name': 'awardEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 15}]}]}, {'Name': 'silenceEnd', 'Value': [{'Name': 'SilenceAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': 'Persons', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}]}, {'Name': 'authorizeEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1909074', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 1575}]}]}, {'Name': 'inoutEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1608621341}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1608621463}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1608621493}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1608623171}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1608621600}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1608623175}]]}, {'Name': 'Identity', 'Value': 3}]}]}, {'Name': 'kickoutEnd', 'Value': [{'Name': '28956248', 'Value': [[{'Name': 'Duration', 'Value': 0}, {'Name': 'Time', 'Value': 1608623171}]]}]}, {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}, {'Name': 'MuteAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}]}, {'Name': 'equipmentsEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1800}]}]}, {'Name': '1909074', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'awCI8tHdTbW4tWMWdWXhiA=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 27693}

str002 = {'ts': 6908989279741935815, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary5', 'o': [{'Name': '_id', 'Value': '5fe1a925f3c5233407490799'}, {'Name': 'ActionTime', 'Value': 1608624421}, {'Name': 'CID', 'Value': 260605243}, {'Name': 'CourseID', 'Value': 121402475}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1608624331}, {'Name': 'StartTime', 'Value': 1608621600}, {'Name': 'SID', 'Value': 1153410}, {'Name': 'Data', 'Value': [{'Name': 'stageEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'UpTotal', 'Value': 1800}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 2}, {'Name': 'DownTotal', 'Value': 0}]}, {'Name': '1909074', 'Value': [{'Name': 'UpTotal', 'Value': 1575}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 1}, {'Name': 'DownTotal', 'Value': 0}]}]},{'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': [38]}]}, {'Name': 'handsupEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'CTime', 'Value': 3}, {'Name': 'Total', 'Value': 1}]}]}, {'Name': 'sharewidgetEnd', 'Value': [{'Name': 'Files', 'Value': [[{'Name': 'EndTime', 'Value': 1608621835}, {'Name': 'FileId', 'Value': '192619485-1153410'}, {'Name': 'Type', 'Value': 2}, {'Name': 'StartTime', 'Value': 1608621696}, {'Name': 'FileName', 'Value': '589d8a8e441511eb8d8e00163e2eb842.mp4'}], [{'Name': 'EndTime', 'Value': 1608624300}, {'Name': 'FileId', 'Value': '192619495-1153410'}, {'Name': 'Type', 'Value': 1}, {'Name': 'StartTime', 'Value': 1608621629}, {'Name': 'FileName', 'Value': '6015819a441511eb97ae00163e2eb842.pptx'}]]}, {'Name': 'Count', 'Value': 2}, {'Name': 'Total', 'Value': 2810}]}, {'Name': 'awardEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 15}]}]}, {'Name': 'silenceEnd', 'Value': [{'Name': 'SilenceAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': 'Persons', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}]}, {'Name': 'authorizeEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}, {'Name': '1909074', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 1575}]}]}, {'Name': 'inoutEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1608621341}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1608621463}], [{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1608621493}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1608623171}]]}, {'Name': 'Identity', 'Value': 1}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1608621600}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1608623175}]]}, {'Name': 'Identity', 'Value': 3}]}]}, {'Name': 'kickoutEnd', 'Value': [{'Name': '28956248', 'Value': [[{'Name': 'Duration', 'Value': 0}, {'Name': 'Time', 'Value': 1608623171}]]}]}, {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}, {'Name': 'MuteAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}]}, {'Name': 'equipmentsEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1800}]}]}, {'Name': '1909074', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'awCI8tHdTbW4tWMWdWXhiA=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 27693}
str002 = {'ts': 6908989279741935815, 'v': 2, 'op': 'i', 'ns': 'hamster.ClassSummary5', 'o': [{'Name': '_id', 'Value': '5fe1a925f3c5233407490799'}, {'Name': 'ActionTime', 'Value': 1608624421}, {'Name': 'CID', 'Value': 260605243}, {'Name': 'CourseID', 'Value': 121402475}, {'Name': 'Cmd', 'Value': 'End'}, {'Name': 'CloseTime', 'Value': 1608624331}, {'Name': 'StartTime', 'Value': 1608621600}, {'Name': 'SID', 'Value': 1153410}, {'Name': 'Data', 'Value': [{'Name': 'stageEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'UpTotal', 'Value': 1800}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 2}, {'Name': 'DownTotal', 'Value': 0}]}, {'Name': '1909074', 'Value': [{'Name': 'UpTotal', 'Value': 1575}, {'Name': 'DownCount', 'Value': 0}, {'Name': 'UpCount', 'Value': 1}, {'Name': 'DownTotal', 'Value': 0}]}]},{'Name': 'screenshareEnd', 'Value': [{'Name': 'Count', 'Value': 1}, {'Name': 'Total', 'Value': 38}, {'Name': 'Period', 'Value': []}]}, {'Name': 'handsupEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'CTime', 'Value': 3}, {'Name': 'Total', 'Value': 1}]}]},  {'Name': 'awardEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 15}]}]},  {'Name': 'kickoutEnd', 'Value': [{'Name': '28956248', 'Value': [[{'Name': 'Duration', 'Value': 0}, {'Name': 'Time', 'Value': 1608623171}]]}]}, {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Total', 'Value': 1800}]}, {'Name': '1909074', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}, {'Name': 'MuteAll', 'Value': [{'Name': 'Count', 'Value': 0}, {'Name': 'Total', 'Value': 0}]}]}, {'Name': 'equipmentsEnd', 'Value': [{'Name': '28956248', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1800}]}]}, {'Name': '1909074', 'Value': [{'Name': 'Camera', 'Value': [{'Name': 'Total', 'Value': 1575}]}]}]}]}], 'o2': '', 'lsid': {'id': {'Kind': 4, 'Data': 'awCI8tHdTbW4tWMWdWXhiA=='}, 'uid': '47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='}, 'txnNumber': 27693}
# def run(string):
#
#     commDataDict = {}
#     totalList = []
#     tableName = "ClassDetails"
#
#     for val in string["o"]:
#         if not isinstance(val["Value"], list):
#             commDataDict.update({val["Name"]: val["Value"]})
#     for val in string["o"]:
#         if val["Name"] == "Data":
#             for val in val["Value"]:
#                 print("---------------------------->1", val)
#                 tmpList = handleDetailsKeyData(val,"insert")
#                 for valdict in tmpList:
#                     totalList.append(dict(valdict, **commDataDict))
#     print(totalList)
# run(str002)
# getClassDetailsUpdateOperation(str002)
getClassSummaryNum(str002)
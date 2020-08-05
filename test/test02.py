import re
import phpserialize
from collections import abc

import json,os,sys

str01 = '''a:2:{s:2:"in";a:5:{i:0;s:10:"1464070293";i:1;s:10:"1464070611";i:2;s:10:"1464070950";i:3;s:10:"1464071656";i:4;s:10:"1464072082";}s:3:"out";a:5:{i:0;s:10:"1464070559";i:1;s:10:"1464070945";i:2;s:10:"1464071402";i:3;s:10:"1464072077";i:4;s:10:"1464072532";}}'''
str02 = '{"title":{"img":"20180301\/507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0.3},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"recordBitRatePlus":false,"echoCancellationDisabled":false,"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":false,"AllStudentsToFreeRegion":true,"ReplaceAll":false,"RewardAll":true,"AuthorityAll":false},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"commentWindow":{"CommentVisible":true},"clouddisk":{"teacherDefaultTab":"AuthorizedResources","limitStudentsCloseCourseWare":false},"classroomWindow":{"student":{"FrontLock":false,"ScreenMark":false},"teacher":{"ExtendClassTime":false,"CameraMirroring":false,"LockBlackboardElement":false,"Win7AeroThemeRecording":false,"MoveStudentOut":true}},"help":{"studentsShow":false},"chatWindow":{"QuestionVisible":true,"EnableSnapshot":true,"MinTimespan":0},"screenShare":{"studentsControlTeacher":false,"ScreenShareMemberLimit":35},"handsupWindow":{"visible":true},"blackboard":{"limitStudentsScroll":false},"dropBlackboardAuthority":false,"dropBackStageCancelAuthority":false,"SmallBlackboardMemberLimit":35,"boardToolbar":{"teacher":{"MiniToolbox":true,"MiniTools":[]},"student":{"Roster":true}}}'
str03 = '''a:5:{s:2:"in";a:2:{i:0;s:10:"1594891562";i:1;s:10:"1594891975";}s:13:"platform_type";a:2:{i:0;i:301;i:1;i:301;}s:7:"os_type";a:2:{i:0;i:4;i:1;i:4;}s:3:"out";a:2:{i:0;s:10:"1594891676";i:1;s:10:"1594892246";}s:11:"exit_status";a:2:{i:0;s:2:"56";i:1;s:3:"111";}}'''
str04 = '''a:2:{s:2:"in";a:1:{i:0;s:10:"1467868772";}s:3:"out";a:1:{i:0;s:10:"1467869025";}}'''

#迭代器；json字符串；嵌套字典的数据读取
def nestedDictIter(nested):
    for key, value in nested.items():
        # if isinstance(key,bytes):
        #    key = key.decode()
        # if isinstance(key,int):
        #     key = "{key}".format(key = key)
        # if isinstance(value, bytes):
        #     value = value.decode()
        # if isinstance(value,int):
        #     value = "{value}".format(value = value)
        if isinstance(value, abc.Mapping):
            #yield from nested_dict_iter(value)
            for k2 in nestedDictIter(value):
               # if isinstance(k2,int):
               #    k2 = str(k2)
               yield (key,) + k2

        else:
            yield key, value

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
        # strToByte = bytes(jsonStr, encoding="utf8")
        # byteToDict = phpserialize.loads(strToByte)
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
            keyname = "json_" + "_".join(i[:-1])

        valuename = i[-1]
        keyList.append(keyname)
        valuesList.append(valuename)

    # print(keyList)
    # print(valuesList)
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
        print("---------------->",jsonStr)
        with open("./logs/error_json.txt","a+") as f:
            f.write("\n")
            f.write(jsonStr)
        return []
    return totalList


# print(jsonToList(str01,11,"phpjson"))
# print("json--------->",jsonToList(str02,11,"json"))
# # print(jsonToList(str03,11,"phpjson"))
# print("phpjson----->",jsonToList(str04,11,"phpjson"))



str07 = {'db': 'test', 'table': 'eeo_class_skin', 'event_type': 1, 'data': {'class_skin_id': '1001', 'school_uid': '0', 'skin_name': '默认皮肤', 'skin_info': '{"title":{"img":"20180301\\/507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"20180807\\/1c075d1d79c163154303.jpeg","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":true},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"chatWindow":{"QuestionVisible":true},"commentWindow":{"CommentVisible":true}}', 'add_time': '1516607614', 'up_time': '1516607614'}, 'updated_data': {}}

str09 = {'db': 'test', 'table': 'eeo_class_member_time', 'event_type': 1, 'data': {'id': '1814', 'school_uid': '1000958', 'course_id': '775', 'class_id': '17242', 'member_uid': '1001566', 'member_account': '23672340108', 'member_nickname': 't8_change', 'time_list': 'a:3:{s:2:"in";a:29:{i:0;s:10:"1478249313";i:1;s:10:"1478249367";i:2;s:10:"1478249400";i:3;s:10:"1478249488";i:4;s:10:"1478250346";i:5;s:10:"1478250368";i:6;s:10:"1478250401";i:7;s:10:"1478250470";i:8;s:10:"1478250482";i:9;s:10:"1478250530";i:10;s:10:"1478250613";i:11;s:10:"1478250805";i:12;s:10:"1478250848";i:13;s:10:"1478250914";i:14;s:10:"1478251506";i:15;s:10:"1478251977";i:16;s:10:"1478252085";i:17;s:10:"1478252183";i:18;s:10:"1478252365";i:19;s:10:"1478252412";i:20;s:10:"1478252484";i:21;s:10:"1478252593";i:22;s:10:"1478252615";i:23;s:10:"1478252679";i:24;s:10:"1478252805";i:25;s:10:"1478253168";i:26;s:10:"1478253543";i:27;s:10:"1478253900";i:28;s:10:"1478255297";}s:3:"out";a:29:{i:0;s:10:"1478249363";i:1;s:10:"1478249393";i:2;s:10:"1478249484";i:3;s:10:"1478249517";i:4;s:10:"1478250364";i:5;s:10:"1478250384";i:6;s:10:"1478250414";i:7;s:10:"1478250475";i:8;s:10:"1478250523";i:9;s:10:"1478250597";i:10;s:10:"1478250782";i:11;s:10:"1478250842";i:12;s:10:"1478250891";i:13;s:10:"1478250963";i:14;s:10:"1478251972";i:15;s:10:"1478252070";i:16;s:10:"1478252160";i:17;s:10:"1478252362";i:18;s:10:"1478252408";i:19;s:10:"1478252479";i:20;s:10:"1478252574";i:21;s:10:"1478252602";i:22;s:10:"1478252675";i:23;s:10:"1478252739";i:24;s:10:"1478253163";i:25;s:10:"1478253187";i:26;s:10:"1478253581";i:27;s:10:"1478255282";i:28;s:10:"1478255322";}s:11:"exit_status";a:29:{i:0;s:1:"1";i:1;s:1:"1";i:2;s:1:"1";i:3;s:1:"1";i:4;s:1:"1";i:5;s:1:"1";i:6;s:1:"1";i:7;s:1:"1";i:8;s:1:"1";i:9;s:1:"3";i:10;s:1:"1";i:11;s:1:"1";i:12;s:1:"1";i:13;s:1:"1";i:14;s:1:"1";i:15;s:1:"1";i:16;s:1:"1";i:17;s:1:"3";i:18;s:1:"1";i:19;s:1:"1";i:20;s:1:"3";i:21;s:1:"1";i:22;s:1:"1";i:23;s:1:"1";i:24;s:1:"3";i:25;s:1:"3";i:26;s:1:"1";i:27;s:1:"3";i:28;s:1:"1";}}', 'is_late': '1', 'is_on': '0', 'is_early': '1', 'identity': '0', 'platform_type': '2', 'stayin_time': '0', 'add_time': '1478249313', 'client_class_id': '261511'}, 'updated_data': {}}

# str07 = {"db": "test", "table": "eeo_class_skin", "event_type": 1, "data": {"class_skin_id": "1001", "school_uid": "0", "skin_name": "默认皮肤", "skin_info": "{"title":{"img":"20180301507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"20180807\\/1c075d1d79c163154303.jpeg","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":true},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"chatWindow":{"QuestionVisible":true},"commentWindow":{"CommentVisible":true}}", "add_time": "1516607614", "up_time": "1516607614"}, "updated_data": {}}


# def getResultSaveCsv(updateDic,hapTableName ,filedName, jsonType,num):
def getMUTLResultOrJson(updateDic ,filedName ="" , jsonType = "json",num = 1):
    '''
    用于多个insert sql拼接
    :param updateDic:
    :param filedName:
    :param jsonType:
    :param num:
    :return: 返回list 列表
    '''
    keyList = []
    valuesList = []
    jsontoList = []
    formatDict = ()
    if num == 2:  # 更新
        for k, v in updateDic["data"]["after"].items():
            keyList.append(k)
            valuesList.append(v)
    elif num == 1:  # insert
        for k, v in updateDic["data"].items():
            if k == filedName:
                jsontoList = jsonToList(v, k, jsonType= jsonType)
            else:
                keyList.append(k)
                valuesList.append(v)
    else:
        pass

    jsontoListLen = len(jsontoList)
    listIndictList = []
    if len(jsontoList) != 0:
        tmpkeyList = keyList + jsontoList[0]
        # print("------------",tmpkeyList)
        for i in range(jsontoListLen - 1):
            tempvaluesSqlList = valuesList + jsontoList[i + 1]
            # print("headers : ",tmpkeyList)

            listIndictList.append(dict(zip(tmpkeyList, tempvaluesSqlList)))
        print(listIndictList)
    else:
        formatDict = dict(zip(keyList, valuesList))
        listIndictList.append(formatDict)
        print("headers : ", keyList)

    print(listIndictList)
    return listIndictList


str10 = {'db': 'test', 'table': 'eeo_class_member_time', 'event_type': 1, 'data': {'id': '127496083', 'school_uid': '2574554', 'course_id': '42610507', 'class_id': '83926837', 'member_uid': '1386822', 'member_account': '23760179273', 'member_nickname': 'Teacher "MAV"', 'time_list': 'a:5:{s:2:"in";a:1:{i:0;s:10:"1578482983";}s:13:"platform_type";a:1:{i:0;i:2;}s:7:"os_type";a:1:{i:0;i:3;}s:3:"out";a:1:{i:0;s:10:"1578483613";}s:11:"exit_status";a:1:{i:0;s:1:"1";}}', 'is_late': '0', 'is_on': '0', 'is_early': '1', 'identity': '3', 'platform_type': '2', 'stayin_time': '0', 'add_time': '1578482984', 'client_class_id': '83926837'}, 'updated_data': {}}

getMUTLResultOrJson(str10 ,filedName ="" , jsonType = "json",num = 1)

import csv

def wirteTOCsv(headers,rows,count,sum):

            with open('stocks{}.csv'.format(sum),'a+',encoding="utf8") as f:
                f_csv = csv.DictWriter(f, headers)
                if count == 0:
                    f_csv.writeheader()
                f_csv.writerows(rows)

                if count == 10 :
                    print("插入数据")
        # else:
        #     with open('stocks{}.csv'.format(i),'a+',encoding="utf8") as f:
        #         f_csv = csv.DictWriter(f, headers)
        #         # f_csv.writeheader()
        #         f_csv.writerows(rows)



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


# str07 = {"db": "test", "table": "eeo_class_skin", "event_type": 1, "data": {"class_skin_id": "1001", "school_uid": "0", "skin_name": "默认皮肤", "skin_info": "{"title":{"img":"20180301507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"20180807\\/1c075d1d79c163154303.jpeg","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":true},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"chatWindow":{"QuestionVisible":true},"commentWindow":{"CommentVisible":true}}", "add_time": "1516607614", "up_time": "1516607614"}, "updated_data": {}}


# def getResultSaveCsv(updateDic,hapTableName ,filedName, jsonType,num):
def getResultOrJson(updateDic ,filedName ="" , jsonType = "json",num = 1):
    '''

    :param updateDic:
    :param filedName:
    :param jsonType:
    :param num:
    :return: 返回formatDict 字典
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

    if len(jsontoList) != 0:
        tmpkeyList = keyList + jsontoList[0]
        for i in range(jsontoListLen - 1):
            tempvaluesSqlList = valuesList + jsontoList[i + 1]
            print("headers : ",tmpkeyList)
            formatDict = dict(zip(tmpkeyList, tempvaluesSqlList))
    else:
        formatDict = dict(zip(keyList, valuesList))
        print("headers : ", keyList)

    return formatDict


str08 = {'db': 'test', 'table': 'eeo_class_member_time', 'event_type': 1, 'data': {'id': '400000008', 'school_uid': '6852094', 'course_id': '72142682', 'class_id': '170297026', 'member_uid': '12891254', 'member_account': '15671763103', 'member_nickname': '科初惠.惠台英语.柯文华', 'time_list': 'a:4:{s:2:"in";a:1:{i:0;s:10:"1589608695";}s:13:"platform_type";a:1:{i:0;i:303;}s:7:"os_type";a:1:{i:0;i:7;}s:3:"out";a:1:{i:0;s:10:"1589608702";}}', 'is_late': '0', 'is_on': '1', 'is_early': '0', 'identity': '3', 'platform_type': '2', 'stayin_time': '0', 'add_time': '1589608748', 'client_class_id': '170297026'}, 'updated_data': {}}

print(getResultOrJson(str07 ,"skin_info", "json",1))
print(getResultOrJson(str08 ,"time_list", "phpjson",1))


headers = ['id', 'school_uid', 'course_id', 'class_id', 'member_uid', 'member_account', 'member_nickname', 'is_late', 'is_on', 'is_early', 'identity', 'platform_type', 'stayin_time', 'add_time', 'client_class_id', 'json_in', 'json_platform_type', 'json_os_type', 'json_out']
rows = [{'id': '400000008', 'school_uid': '6852094', 'course_id': '72142682', 'class_id': '170297026', 'member_uid': '12891254', 'member_account': '15671763103', 'member_nickname': '科初惠.惠台英语.柯文华', 'is_late': '0', 'is_on': '1', 'is_early': '0', 'identity': '3', 'platform_type': '2', 'stayin_time': '0', 'add_time': '1589608748', 'client_class_id': '170297026', 'json_in': '1589608695', 'json_platform_type': 303, 'json_os_type': 7, 'json_out': '1589608702'}]
import csv


def wirteTOCsv(headers,rows,count,sum):

            with open('stocks{}.csv'.format(sum),'a+',encoding="utf8") as f:
                f_csv = csv.DictWriter(f, headers)
                if count == 0:
                    f_csv.writeheader()
                f_csv.writerows(rows)

                if count == 10 :
                    print("插入数据")


def run():
    count = 0
    sum = 0
    for i in range(50):
        print(count)
        if count == 0:
            sum += 1
        wirteTOCsv(headers,rows,count, sum)

        if count < 10:
            count += 1
        else:
            count = 0

run()

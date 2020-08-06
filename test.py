import re
import phpserialize
from collections import abc

import json,os,sys

str01 = '''a:2:{s:2:"in";a:5:{i:0;s:10:"1464070293";i:1;s:10:"1464070611";i:2;s:10:"1464070950";i:3;s:10:"1464071656";i:4;s:10:"1464072082";}s:3:"out";a:5:{i:0;s:10:"1464070559";i:1;s:10:"1464070945";i:2;s:10:"1464071402";i:3;s:10:"1464072077";i:4;s:10:"1464072532";}}'''
str02 = '{"title":{"img":"20180301\/507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0.3},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"recordBitRatePlus":false,"echoCancellationDisabled":false,"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":false,"AllStudentsToFreeRegion":true,"ReplaceAll":false,"RewardAll":true,"AuthorityAll":false},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"commentWindow":{"CommentVisible":true},"clouddisk":{"teacherDefaultTab":"AuthorizedResources","limitStudentsCloseCourseWare":false},"classroomWindow":{"student":{"FrontLock":false,"ScreenMark":false},"teacher":{"ExtendClassTime":false,"CameraMirroring":false,"LockBlackboardElement":false,"Win7AeroThemeRecording":false,"MoveStudentOut":true}},"help":{"studentsShow":false},"chatWindow":{"QuestionVisible":true,"EnableSnapshot":true,"MinTimespan":0},"screenShare":{"studentsControlTeacher":false,"ScreenShareMemberLimit":35},"handsupWindow":{"visible":true},"blackboard":{"limitStudentsScroll":false},"dropBlackboardAuthority":false,"dropBackStageCancelAuthority":false,"SmallBlackboardMemberLimit":35,"boardToolbar":{"teacher":{"MiniToolbox":true,"MiniTools":[]},"student":{"Roster":true}}}'
str03 = '''a:5:{s:2:"in";a:2:{i:0;s:10:"1594891562";i:1;s:10:"1594891975";}s:13:"platform_type";a:2:{i:0;i:301;i:1;i:301;}s:7:"os_type";a:2:{i:0;i:4;i:1;i:4;}s:3:"out";a:2:{i:0;s:10:"1594891676";i:1;s:10:"1594892246";}s:11:"exit_status";a:2:{i:0;s:2:"56";i:1;s:3:"111";}}'''
str04 = '''a:2:{s:2:"in";a:1:{i:0;s:10:"1467868772";}s:3:"out";a:1:{i:0;s:10:"1467869025";}}'''


from common.common import nestedDictIter
# 处理field josn语句
def jsonToList01(jsonStr, fieldName,jsonType = "json"):
    '''

    :param jsonStr:
    :param fieldName:
    :param jsonType: 默认json ； phpjson
    :return: list index:0 keyname index:1-n values
    '''
    #转字典
    if jsonType == "json":
        jsonToDict = json.loads(jsonStr)
        #jsonToDict = jsonStr
    elif jsonType == "phpjson":
        phpseriTostr = str(phpserialize.loads(jsonStr.encode(), decode_strings=True))
        print("phpseriTostr",phpseriTostr)
        reStr = re.sub('(?<!^)}(?!$)', "]",
                        re.sub('(?<!^){(?!$)', "[", re.sub('[0-9]+:', '', re.sub('[0-9]+:', '', phpseriTostr)))).replace(
            "\'", "\"").replace(" ", "")
        print("restr",reStr)
        jsonToDict = json.loads(reStr)

    elif jsonType == "listjson":

        json_list = jsonStr.strip("}},{")

        # for i in json_list:
        #     print(i)
    keyList = []
    valuesList = []
    totalList = []
    '''
    调用nested_dict_iter函数 yield
    读取嵌套字典的数据
    '''
    print(keyList)
    print(valuesList)
    for i in nestedDictIter(jsonToDict):
        keyname = "".join(i[:-1])
        if jsonType == "json":
            keyname = "_".join(i[:-1])

        valuename = i[-1]
        keyList.append(keyname)
        valuesList.append(valuename)
    print(valuesList)

    try:
        totalList.append(keyList)
        valListLen = len(valuesList)
        valListElementLen = len(valuesList[0])

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
        # print(jsonStr)
        pass
    return  totalList

str112 = 'a:3:{s:3:"out";a:2:{i:0;s:10:"1474376929";i:1;s:10:"1474377337";}s:11:"exit_status";a:2:{i:0;s:1:"1";i:1;s:1:"1";}s:2:"in";a:1:{i:0;s:10:"1474376933";}}'
# print(jsonToList(str01,11,"phpjson"))
# print("json--------->",jsonToList(str02,11,"json"))
# print(jsonToList(str03,11,"phpjson"))
# print("phpjson----->",jsonToList(str04,11,"phpjson"))

str05 = 'a:3:{s:2:"in";a:2:{i:0;s:10:"1501134167";i:1;s:10:"1501140558";}s:3:"out";a:1:{i:0;s:10:"1501141533";}s:11:"exit_status";a:1:{i:0;s:1:"1";}}'

# from handleserivce.handleJson import jsonToList
from handleserivce.handleJson import jsonToList
print("------>",jsonToList(str05,11,"phpjson"))
# print("------>",jsonToList01(str05,11,"phpjson"))

key =  ['json_in', 'json_out', 'json_exit_status']
value  =  [['1501134167', '1501140558'], ['1501141533'], ['1']]



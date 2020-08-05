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
def jsonToList(jsonStr, fieldName,jsonType = "json"):
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


# print(jsonToList(str01,11,"phpjson"))
# print("json--------->",jsonToList(str02,11,"json"))
# print(jsonToList(str03,11,"phpjson"))
# print("phpjson----->",jsonToList(str04,11,"phpjson"))

# str05 = 'a:4:{s:2:"in";a:9:{i:0;s:10:"1508498691";i:1;s:10:"1508550732";i:2;s:10:"1508550942";i:3;s:10:"1508575529";i:4;s:10:"1508575841";i:5;s:10:"1508576175";i:6;s:10:"1508579091";i:7;s:10:"1508579643";i:8;s:10:"1508580915";}s:3:"out";a:9:{i:0;s:10:"1508499381";i:1;s:10:"1508550942";i:2;s:10:"1508551080";i:3;s:10:"1508575642";i:4;s:10:"1508575855";i:5;s:10:"1508576197";i:6;s:10:"1508579313";i:7;s:10:"1508580897";i:8;s:10:"1508581243";}s:11:"exit_status";a:9:{i:0;s:1:"3";i:1;s:1:"1";i:2;s:1:"3";i:3;s:1:"3";i:4;s:1:"1";i:5;s:1:"1";i:6;s:1:"1";i:7;s:1:"1";i:8;s:1:"1";}s:13:"platform_type";a:6:{i:0;N;i:1;N;i:2;N;i:3;N;i:4;N;i:5;N;}}'
# print(jsonToList(str05,11,"phpjson"))

str06 = {'id': False, 'school_uid': True, 'course_id': False, 'class_id': False, 'member_uid': False, 'member_account': False, 'member_nickname': False, 'time_list': False, 'is_late': False, 'is_on': False, 'is_early': False, 'identity': False, 'platform_type': True, 'stayin_time': False, 'add_time': False, 'client_class_id': False}
# before = {'id': '376965019', 'school_uid': '16015646', 'course_id': '57777211', 'class_id': '176707654', 'member_uid': '17443330', 'member_account': '13818702080', 'member_nickname': '赵羿然Leo', 'time_list': 'a:5:{s:2:"in";a:2:{i:0;s:10:"1589941181";i:1;s:10:"1589942374";}s:13:"platform_type";a:2:{i:0;i:302;i:1;i:302;}s:7:"os_type";a:2:{i:0;i:4;i:1;i:4;}s:3:"out";a:1:{i:0;s:10:"1589942369";}s:11:"exit_status";a:1:{i:0;s:2:"56";}}', 'is_late': '0', 'is_on': '1', 'is_early': '1', 'identity': '1', 'platform_type': '331', 'stayin_time': '0', 'add_time': '1589941182', 'client_class_id': '176707654'}
# before = 'a:5:{s:2:"in";a:2:{i:0;s:10:"1589941181";}s:13:"platform_type";a:2:{i:0;i:302;}s:7:"os_type";a:2:{i:0;i:4;}s:3:"out";a:1:{i:0;s:10:"1589942369";}s:11:"exit_status";a:1:{i:0;s:2:"56";}}'
before = 'a:4:{s:2:"in";a:1:{i:0;s:10:"1589608695";}s:13:"platform_type";a:1:{i:0;i:303;}s:7:"os_type";a:1:{i:0;i:7;}s:3:"out";a:1:{i:0;s:10:"1589608702";}}'
after = 'a:5:{s:2:"in";a:2:{i:0;s:10:"1589608695";i:1;s:10:"1589608747";}s:13:"platform_type";a:2:{i:0;i:303;i:1;i:301;}s:7:"os_type";a:2:{i:0;i:7;i:1;i:7;}s:3:"out";a:1:{i:0;s:10:"1589608702";}s:11:"exit_status";a:1:{i:0;s:1:"1";}}'
# str06 = '''{"id": False, "school_uid": False, "course_id": False, "class_id": False, "member_uid": False, "member_account": False, "member_nickname": False, "time_list": False, "is_late": False, "is_on": False, "is_early": False, "identity": False, "platform_type": True, "stayin_time": False, "add_time": False, "client_class_id": False}'''
str09 = '''a:5:{s:2:"in";a:2:{i:0;s:10:"12008625";i:1;s:10:"1589608747";}s:13:"platform_type";a:2:{i:0;i:303;i:1;i:301;}s:7:"os_type";a:2:{i:0;i:7;i:1;i:7;}s:3:"out";a:1:{i:0;s:10:"1589608702";}s:11:"exit_status";a:1:{i:0;s:1:"1";}}'''

def jsonToList1(jsonStr,jsonType = "json"):
    jsonToDict = dict()
    if jsonType == "json":
        jsonToDict = json.loads(jsonStr)
        #jsonToDict = jsonStr
    elif jsonType == "phpjson":
        try:
            phpseriTostr = str(phpserialize.loads(jsonStr.encode(), decode_strings=True))

            reStr = re.sub('(?<!^)}(?!$)', "]",
                            re.sub('(?<!^){(?!$)', "[", re.sub('[0-9]+:', '', re.sub('[0-9]+:', '', phpseriTostr)))).replace(
                "\'", "\"").replace(" ", "")

            tmpJsonToDict = json.loads(reStr)

            for k,v in tmpJsonToDict.items():
                jsonToDict["josn_"+k] = v
        except ValueError as e:
            print("反序列的值有问题")
            return
    return  jsonToDict

# print("jsonToList1",jsonToList1(after,"phpjson"))


from common.common import findUpdatedFiled
print(findUpdatedFiled(str06))


from comparePhpJson import getListDefferSet

def getJsonKeyupdateDetails(before,after):
    '''

    :param before:
    :param after:
    :return:
    '''
    # filedName = findUpdatedFiled(str06)
    # filedName["in"]

    if before == after:
        return []

    beforeDict = jsonToList1(before, "phpjson")
    afterDict = jsonToList1(after, "phpjson")
    # print(beforeDict)
    # print(afterDict)
    tmpBefore = []
    tmpAfter = []
    #对比before 和after的 字典值，并取得list的值得交集
    for k,v in beforeDict.items():
        tmpBefore.append(k)
    for k,v in afterDict.items():
        tmpAfter.append(k)

    joinFieldsList = [item for item in tmpBefore if item in tmpAfter]
    defferFieldsList = list(set(tmpAfter) ^ set(tmpBefore))

    # totalDict = dict()
    print("joinFieldsList",joinFieldsList)
    print("defferFieldsList",defferFieldsList)
    fieldsList = []
    valList = []
    totalList = []

    for name in joinFieldsList:
        ret = list(set(afterDict[name]) ^ set(beforeDict[name]))
        # print(name,ret,len(ret))
        if len(ret) < 1:
            # totalDict[name] = beforeDict[name][-1]
            fieldsList.append(name)
            valList.append(beforeDict[name][-1])
        else:
            # totalDict[name] = ret
            fieldsList.append(name)
            valList.append(ret[0])
    for addName in defferFieldsList:
        newVal = afterDict[addName]
        # totalDict[addName] = newVal

        fieldsList.append(addName)
        valList.append(newVal[0])

    totalList.append(fieldsList)
    totalList.append(valList)
    print("--------->:",totalList)
    return totalList

str07 = {'db': 'test', 'table': 'eeo_class_skin', 'event_type': 1, 'data': {'class_skin_id': '1001', 'school_uid': '0', 'skin_name': '默认皮肤', 'skin_info': '{"title":{"img":"20180301\\/507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"20180807\\/1c075d1d79c163154303.jpeg","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":true},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"chatWindow":{"QuestionVisible":true},"commentWindow":{"CommentVisible":true}}', 'add_time': '1516607614', 'up_time': '1516607614'}, 'updated_data': {}}

before = 'a:5:{s:2:"in";a:1:{i:0;s:10:"1589941181";}s:13:"platform_type";a:1:{i:0;i:302;}s:7:"os_type";a:1:{i:0;i:4;}s:3:"out";a:1:{i:0;s:10:"1589942369";}s:11:"exit_status";a:1:{i:0;s:2:"56";}}'
# after = 'a:5:{s:2:"in";a:1:{i:0;s:10:"1589941181";}s:13:"platform_type";a:1:{i:0;i:302;}s:7:"os_type";a:1:{i:0;i:4;}s:3:"out";a:1:{i:0;s:10:"1589942369";}s:11:"exit_status";a:1:{i:0;s:2:"56";}}'
after = 'a:5:{s:2:"in";a:2:{i:0;s:10:"1589941181";i:1;s:10:"1589942374";}s:13:"platform_type";a:2:{i:0;i:302;i:1;i:302;}s:7:"os_type";a:2:{i:0;i:4;i:1;i:4;}s:3:"out";a:1:{i:0;s:10:"1589942369";}s:11:"exit_status";a:1:{i:0;s:2:"56";}}'
print(getJsonKeyupdateDetails(before,after)) #更新内容

def getAllFieldName(data=0,updated_data=0):
    jsontoList = getListDefferSet(before,
                                  after)[0]
    print(findUpdatedFiled(str06)+jsontoList)
    print()

getAllFieldName()
def updateOrJsonSql(updateDic, filedName, num):
    '''
    only jsonType="phpjson"
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
    print("-------> ",updateDic["data"])
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
                jsontoList = getListDefferSet(v, k)

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
            print("valuesSqlList001------>:",valuesSqlList)
            print("filedsSqlList001------>:",filedsSqlList)
            #
            SQL = "insert into " + updateDic["table"] + " " + filedsSqlList + " values " + valuesSqlList + ";"
            sqlList.append(SQL)


    # filedsSqlList = str(keyList).replace('[', '(').replace(']', ')').replace('\'', '')
    # valuesSqlList = str(valuesList).replace('[', '(').replace(']', ')')
    else:
        SQL = "insert into " + updateDic["table"] + " " + filedsSqlList + " values " + valuesSqlList + ";"
        sqlList.append(SQL)

    return sqlList



# print(jsonToList1(before,"phpjson"))
# print(jsonToList1(after,"phpjson"))
#
# before = {'in': ['1589941181', '1589942374'], 'platform_type': [302, 302], 'os_type': [4, 4], 'out': ['1589942369'], 'exit_status': ['56']}
# after = {'in': ['1589941181', '1589942374'], 'platform_type': [302, 302], 'os_type': [4, 4], 'out': ['1589942369'], 'exit_status': ['56']}
#

# list1 = [1,2,3,4]
# list2 = [1,2,3,4,5]
# ret = list(set(list2)^set(list1))
#
# print("-------------")
#
# def tes():
#     return 1,1
# print(tes())
#
# print("----------------------------------------------------------")
# list_fileld = ["homework_id","course_id","school_uid","teacher_uid","homework_title","homework_desc","image","video","audio","docs","problems_ids","status","is_open","is_revise","is_del","is_download","open_type","score_type","score_value","end_time","start_time","update_time","add_time"]
# for i in list_fileld:
#     print("try:")
#     print("    {i} = valDict[\"{i}\"]".format(i = i))
#     print("except KeyError as e:")
#     print("    {i} = \"0\"".format(i = i))
#
list_dict = '{"src":"/upload/homework/images/20190426/8b0c59aca9eefc5d4749.jpg","source":' \
            '{"path":"upload/homework/images/","viewsrc":{"Lpic":"","Mpic":"","Spic":"20190426/8b0c59aca9eefc5d4749_200.jpg"},' \
            '"src_source":"20190426/8b0c59aca9eefc5d4749.jpg","edb":"","src":"20190426/8b0c59aca9eefc5d4749.jpg"}},' \
            '{"src":"/upload/homework/images/20190427/19d62593448e211b2000.jpg","source":{"path":"upload/homework/images/",' \
            '"viewsrc":{"Lpic":"","Mpic":"","Spic":"20190427/19d62593448e211b2000_200.jpg"},"src_source":"20190426/8b9c4d72a80ebb314575.jpg",' \
            '"edb":"","src":"20190427/19d62593448e211b2000.jpg"}},{"src":"/upload/homework/images/20190426/b8ef34c6919412a23076.jpg",' \
            '"source":{"path":"upload/homework/images/","viewsrc":{"Lpic":"","Mpic":"","Spic":"20190426/b8ef34c6919412a23076_200.jpg"},' \
            '"src_source":"20190426/b8ef34c6919412a23076.jpg","edb":"","src":"20190426/b8ef34c6919412a23076.jpg"}},' \
            '{"src":"/upload/homework/images/20190427/c1817a694b913e9e7757.jpg","source":{"path":"upload/homework/images/",' \
            '"viewsrc":{"Lpic":"","Mpic":"","Spic":"20190427/c1817a694b913e9e7757_200.jpg"},' \
            '"src_source":"20190427/c1817a694b913e9e7757.jpg","edb":"","src":"20190427/c1817a694b913e9e7757.jpg"}}'

# print("phpjson----->",jsonToList(list_dict,11,"listjson"))

# print(json.loads(list_dict))

import emoji




content = '\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974\\U0001f974'


tmplist = ['time_list', 'platform_type', 'josn_in', 'josn_platform_type', 'josn_os_type', 'josn_out', 'josn_exit_status']

ll = [index for index,val in enumerate(tmplist) if val == "platform_type"]

print(ll)
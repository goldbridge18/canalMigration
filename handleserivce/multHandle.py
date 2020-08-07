import datetime

from handleserivce.handleJson import jsonToList
from dbconn.mysqlConn import execCmd

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

    keyList.append("operation_type")
    valuesList.append(updateDic["event_type"])

    keyList.append("execute_time")
    valuesList.append(updateDic["execute_time"])

    if num == 2:  # 更新
        for k, v in updateDic["data"]["after"].items():
            keyList.append(k)
            valuesList.append(v)

    elif num == 1:  # insert
        for k, v in updateDic["data"].items():
            if k == filedName:
                jsontoList = jsonToList(v, k, jsonType = jsonType)
            else:
                keyList.append(k)
                valuesList.append(v.replace("\"","").replace("\'",""))
    else:
        pass
    # print(jsontoList)
    jsontoListLen = len(jsontoList)
    # print(jsontoListLen)
    listIndictList = []
    if len(jsontoList) != 0:
        tmpkeyList = keyList + jsontoList[0]
        for i in range(jsontoListLen - 1):
            tempvaluesSqlList = valuesList + jsontoList[i + 1]
            listIndictList.append(dict(zip(tmpkeyList, tempvaluesSqlList)))
    else:
        formatDict = dict(zip(keyList, valuesList))
        listIndictList.append(formatDict)
    # print("listIndictList---->",listIndictList)
    return listIndictList


def multisql(val,header,count,size, flag):
    '''
    批量插入数据
    :param val:
    :param count:
    :param flag:
    :return:
    '''

    headerStr = header
    if count == size:
        flag = True
    if flag :

       sql1 = headerStr + str(val).replace("[\"","").replace("\"]","").replace("\"","")
       print("----------",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"------------------")
       print("--------------------------插入数据----------------------------")
       execCmd(sql1)
       # print(sql1)
       print("--------------------------插入完成----------------------------")

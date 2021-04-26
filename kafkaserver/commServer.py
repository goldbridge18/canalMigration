import json

from collections import  abc
from dbconn.mysqlConn import execCmd,concurExecSql

def getDictMaxLayer(dictData):
    '''
    获取 字典 dict的层数
    :param dictData:
    :return: int
    '''
    return max(getDictMaxLayer(v) if isinstance(v,abc.Mapping) else 0 for v in dictData.values()) + 1

def nestedStrToDictIter(nested):
    for key, value in nested.items():
        # print(key,value)
        if isinstance(value, abc.Mapping):
            # yield from nested_dict_iter(value)
            # print("-------",value)
            for k2 in nestedStrToDictIter(value):
                if isinstance(k2, int):
                    k2 = str(k2)
                yield (key,) + k2
        elif isinstance(value, list) and isinstance(value[0],abc.Mapping):
            for val in value:
                yield from nestedStrToDictIter(val)

        else:
            if isinstance(value,list):
                value = str(tuple(value)).replace("\'","")
            yield key, value

#字符串是json格式的
def handleStringJson(string):
    '''

    :param string:
    :return:
    '''
    totalDict = {}
    tmpDict = {}
    for key,val in string.items():
        # print(key, val)
        try:
            if isinstance(json.loads(val),abc.Mapping):
                # for i in nestedStrToDictIter(json.loads(val)):
                #     tmpDict.update({key + "_" + i[-2]: i[-1]})
                # print("-----------------------111",tmpDict)
                # totalDict.update(key,str(tmpDict))
                pass
            else:
                totalDict.update({key:val})
        except Exception as e:
            totalDict.update({key:val})

    return  totalDict

##
def nestedMongKafkaJsonToList(nested):
    '''
    递归或获取 key 是Name、Value的值
    :param nested:
    :return:
    '''
    if isinstance(nested["Value"],list) :
         # print("---------->11",nested["Value"])
         if  len(nested["Value"]) != 0:
            for val in nested["Value"]:
                # print("---",val)
                if isinstance(val,list):
                    for i in val:
                        # print(i)
                        if isinstance(i["Value"],list):
                            if len(i["Value"]) != 0:
                                yield from nestedMongKafkaJsonToList(i)
                        else:
                            yield from nestedMongKafkaJsonToList(i)
                elif isinstance(val,abc.Mapping):
                    yield from nestedMongKafkaJsonToList(val)
    else:
        for key, value in nested.items():
            if isinstance(value, list) and isinstance(value[0],abc.Mapping):
                for val in value:
                    yield from nestedMongKafkaJsonToList(val)

            elif isinstance(value, list) and isinstance(value[0], list) :
                for i in value[0]:
                    if isinstance(i["Value"],list) and  len(i["Value"]) ==0:
                        pass
                    else:

                        for va in  nestedMongKafkaJsonToList(i):
                            print("-----------------------------error-------")
            else:
                yield value


def handleJsonTosql(string,tableNameKey,keyName = "",commDataDict = {},context = ""):
    '''

    :param string:
    :param keyName:  keyName = tablename
    :return:
    '''
    #data 的key的值处理
    addTmpDict = {}
    totalList = []
    sqlList = []
    totalFieldsList = []
    tableName = "eeo_{table}_".format(table=tableNameKey) + keyName.lower()
    for valdict in string :
        for key,val in valdict.items():
            if key.isdigit():
                UID = key
                addTmpDict.update({"Uid":key})
            # print([dict(x,**addTmpDict) for x in val ])
                totalList += [dict(x,**addTmpDict) for x in val ]
            else:
                totalList = string
    #print("sql---------->:",totalList)
    for val in totalList:
        fieldsList = []
        valuesList = []

        if len(val) == 0:
            pass
        else:
            # print("----------------------->",val)
            # if tableNameKey == "classsummary":
            #     tmpKeyList = [keyName.lower() +  '_' + x for x in  list(val.keys())]
            #     val = dict(zip(tmpKeyList,list(val.values())))

            addDict = dict(val,**commDataDict)
            fieldsList.append(tuple([k for k, v in addDict.items()]))
            valuesList.append(tuple([v for k, v in addDict.items()]))
            # totalFieldsList += fieldsList[0]
            # totalFieldsList.append(tableName)
            if len(fieldsList) != 0:
                #print("------",str(tuple(fieldsList[0])))
                fieldsStr = str(tuple(fieldsList[0])).replace(" ",'').replace("\\n\'","").replace("\\n","").replace("\"","\'").replace("\'", "`").replace("_id","id").replace(",)",")").lower()
                #print("------------",valuesList[0])
                valuesStr = str(valuesList[0]).replace("[", "(").replace("]", ")").replace("None", "").replace("\"[","(").replace("]\"", ")").\
                    replace("()","\"\"").replace("({","\"").replace("})","\"")

                #print( tableName,"------fieldsList----------1", fieldsStr)
                #print( tableName,"---------valuesList-------1", valuesStr)


                query = "insert into " + tableName + fieldsStr +" value" + valuesStr + ";"
                # totalFieldsList.append(query)
                # print(query)
                #execCmd(query,context)
                sqlList.append(query)


            else:
                print(tableName,"------fieldsList----------2", fieldsList)
                print(tableName,"---------valuesList-------2", valuesList)
                # pass

    #并行执行sql
    concurExecSql(sqlList)
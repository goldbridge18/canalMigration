import time
import re, datetime,json
from canal.client import Client
from canal.protocol import EntryProtocol_pb2
from canal.protocol import CanalProtocol_pb2

from handleserivce.handleJson import *
from handleserivce.compareUpdateData import *
from dbconn.mysqlConn import *
from handleserivce.multHandle import multisql
from handleserivce.tablestructe import tableStruncte,getMUTLResultOrJson
from handleserivce.logTableEntity import LogTableEntity
from common.formatDateServer import formatDate
from common.common import findUpdatedFiled
from handleserivce.multHandle import getMUTLResultOrJson01


'''
需要安装的包：
pip install canal-python
pip install protobuf
pip install google-cloud-translate
pip install google-cloud 
pip install --upgrade google-api-python-client
'''

#参数值设置：

cfg = ConfigParser()
cfg.read("conf/setting.cnf")

databaseName = cfg.get('databaseInfo','databaseName')
tableName = cfg.get('databaseInfo','tableName')
fieldName = cfg.get('databaseInfo','fieldName')
# hadTableName = cfg.get('databaseInfo','hadTableName')
jsonType = cfg.get('databaseInfo','jsonType')
tableList = []
tableDict = json.loads(tableName)
for key,value in tableDict.items():
    tableList.append(key)

print(tableList)
#批量生成insert
rowNum = cfg.getint('dataInfo','rowNum')
isSqlBatch = cfg.getint('dataInfo','isSqlBatch')

count = 1 #使用生成批量sql的计数
flag = False
totalList = []

#canal client info
client_id = bytes("{client_id}".format(client_id=cfg.getint('canalInfo','client_id')).encode("utf8"))
destination = bytes("{destination}".format(destination=cfg.get('canalInfo','destination')).encode("utf8"))

#获取指定的数据量
batchSize = cfg.getint('canalInfo','batchSize')

# canal建立连接
client = Client()
client.connect(host=cfg.get('canalInfo','host'), port=cfg.getint('canalInfo','port'))
client.check_valid(username=b'', password=b'')
client.subscribe(client_id=client_id, destination=destination, filter=b'.*\\..*')

# while循环执行读取canalserver数据
while True:
    message = client.get(batchSize)
    entries = message['entries']
    for entry in entries:
        entry_type = entry.entryType
        if entry_type in [EntryProtocol_pb2.EntryType.TRANSACTIONBEGIN, EntryProtocol_pb2.EntryType.TRANSACTIONEND]:
            continue
        row_change = EntryProtocol_pb2.RowChange()
        row_change.MergeFromString(entry.storeValue)
        event_type = row_change.eventType
        header = entry.header
        database = header.schemaName
        table = header.tableName
        event_type = header.eventType
        for row in row_change.rowDatas:
            format_data = dict()
            updated_fields = dict()
            if event_type == EntryProtocol_pb2.EventType.DELETE:
                for column in row.beforeColumns:
                    # format_data = {
                    #     column.name: column.value
                    # }
                    format_data[column.name] = column.value
            elif event_type == EntryProtocol_pb2.EventType.INSERT:
                for column in row.afterColumns:
                    format_data[column.name] = column.value
                    #format_data.setdefault(column.name,column.value)
            elif event_type == EntryProtocol_pb2.EventType.ALTER:
                format_data[column.name] = column.value
            else:
                format_data['before'] = dict()
                format_data['after'] = dict()
                for column in row.beforeColumns:
                    format_data['before'][column.name] = column.value
                for column in row.afterColumns:
                    format_data['after'][column.name] = column.value
                    updated_fields[column.name] = column.updated  # 获取update的字段信息

            data = dict(
                db=database,
                table=table,
                event_type=event_type,
                data=format_data,
                updated_fields=updated_fields,  # 获取update的字段信息

            )

            # --------------------数据处理-------------------------------------------
            # print(updated_fields)
            # print(data)
            # getUpdatedFieldsValue(data)
            data.setdefault("updated_fields",data["updated_fields"])
            #获取binlog的logfile，posistion、binlog的执行时间
            binlogInfo = dict()
            binlogInfo.setdefault("logfile_name",header.logfileName)
            binlogInfo.setdefault("logfile_Offset",header.logfileOffset)
            binlogInfo.setdefault("execute_time",formatDate(header.executeTime))
            binlogInfo.setdefault("operation_type",header.eventType)

            # data.setdefault("execute_time",formatDate(header.executeTime))
            data.setdefault("execute_time",round(header.executeTime/1000))

            if data['db'] == databaseName and data['table'] in tableList:
                tableName = data['table']
                # tableHeader
                table_header = data['table'] + "_header"
                # mysql表对应hive表的表名
                hadTableName = tableDict[data['table']]

                # 获取sql
                if event_type == EntryProtocol_pb2.EventType.INSERT:
                    # 获取insert语句的数据
                    if len(jsonType) == 0:

                       if isSqlBatch == 1:
                           get_function = getattr(tableStruncte, tableName)
                           val = get_function(getMUTLResultOrJson01(data, fieldName, jsonType))
                           totalList.append(val)
                           multisql(totalList, getattr(tableStruncte, table_header), count, rowNum, flag)
                           if count < rowNum:
                               count += 1
                           else:
                               count = 1
                               flag = False
                               totalList = []

                       else: # 单条解析

                            print("-----------------insert---2-----------------")
                            res = getSql(data, hadTableName, jsonType, fieldName)
                            execCmd(res)
                            # print(res)
                    else:
                        if isSqlBatch == 1 : #批量
                        # if False : #批量
                            # 获取的批量插入的值
                            res = ""
                            print("-------------------------------------2----------------")
                            # getMUTLResultOrJson01(data, fieldName, jsonType)
                            get_function = getattr(tableStruncte, tableName)
                            val = get_function(getMUTLResultOrJson01(data, fieldName, jsonType))
                            totalList.append(val)
                            # print("---->totalList", totalList)
                            multisql(totalList, getattr(tableStruncte, table_header), count, rowNum, flag)
                            print("-------------------------------------2----------------")
                            # val = tableStruncte.eeo_class_member_time(getMUTLResultOrJson(data, fieldName, jsonType, 1))
                            # get_function = getattr(tableStruncte,"eeo_class_member_time")
                            # val = get_function(getMUTLResultOrJson(data, fieldName, jsonType, 1))
                            # totalList.append(val)
                            # multisql(totalList,getattr(tableStruncte,table_header), count,rowNum, flag) #判断是否插入
                            if count < rowNum:
                                count += 1
                            else:
                                count = 1
                                flag = False
                                totalList = []
                        else: #单条insert

                            print("---------------insert--json---------------------")
                            res = getSql(data, hadTableName, jsonType, fieldName)
                            execCmd(res)
                            # print(res)
                            # res = includeJsonSql(data,hadTableName,fieldName,jsonType, 1)

                elif event_type == EntryProtocol_pb2.EventType.UPDATE:

                    if fieldName in findUpdatedFiled(data["updated_fields"]) or len(jsonType) > 0:

                        print("---------------update--1---------------------")
                        '''
                        #没哟解析
                        res = getSql(data, hadTableName)
                        # execCmd(res)
                        print(res)
                        # # res = parseUpdateJsonToSql(data, fieldName,hadTableName)
                        '''
                        res = getSql(data, hadTableName,jsonType, fieldName)
                        execCmd(res)
                        # print(res)
                        #解析之后
                        # get_function = getattr(LogTableEntity, tableName)
                        # val = get_function(fieldsValueToDict(data, jsonType, fieldName))
                        # totalList.append(val)
                        # multisql(totalList, getattr(LogTableEntity, table_header), count, 1, flag)

                    else:
                        # res = includeJsonSql(data, fieldName, 2)
                        # res  = updateAndInsertSql(data,hadTableName)
                        print("---------------update--2---------------------")
                        res1 = getSql(data, hadTableName, jsonType, fieldName)
                        execCmd(res1)
                        # print(res1)
                        # get_function = getattr(LogTableEntity, tableName)
                        # val = get_function(fieldsValueToDict(data, jsonType, fieldName))
                        # totalList.append(val)
                        # multisql(totalList, getattr(LogTableEntity, table_header), count, 1, flag)

                elif event_type == EntryProtocol_pb2.EventType.DELETE:

                    if len(jsonType) == 0:

                        print("--------------delete----1-------------------")
                        res = getSql(data, hadTableName, jsonType, fieldName)
                        # print(res)
                        execCmd(res)
                    else:
                        print("--------------delete----2-------------------")
                        #解析之后
                        res = getSql(data, hadTableName, jsonType, fieldName)
                        execCmd(res)
                        # print(res)
                        # print("--------------delete----3-------------------")
                        '''
                        #没有解析
                        res1 = getSql(data,hadTableName)
                        # execCmd(res)
                        print(res1)
                        # res = includeJsonSql(data, hadTableName, fieldName, jsonType, 1)
                        '''
            else:

                pass
    time.sleep(0.001)

client.disconnect()


import  json,re
from kafkaserver.handleSummary import getClassSummaryNum
from kafkaserver.handleDetails import getClassDetailsData
from kafkaserver.handleDetails import getClassDetailsUpdateOperation

from kafka import KafkaConsumer
from kafka import TopicPartition

global null ,false ,true
null = ""
false = 0
true = 1

consumer = KafkaConsumer( group_id='mongo-group1', bootstrap_servers=['10.0.0.64:9092'])
consumer.assign([TopicPartition(topic= 'mongodb-tes', partition= 0)])
print("-----------welcome use kafka ---------------")
for message in consumer:
    # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
    data = eval(str(message.value, encoding="utf8"))

    try:
        tableName = re.search('ClassDetails_|ClassSummary',data["ns"]).group()
    except AttributeError as e:
        tableName = ''

    if tableName == "ClassDetails_":
        # print("--------------------------------------------",tableName)
        # print(data)
        if data["op"] == "i":
            pass
            print("--------insert----------", data["ns"])
            getClassDetailsData(data)
            # print(data)
            # print(getClassDetailsData(data))
            # for i in getClassDetailsData(data):
            #     from dbconn.mysqlConn import execCmd
            #     query = ""
            #     print(query)
            #     execCmd(i,data)
        elif data["op"] == "u":
            pass
            # print("--------update----------", data)
            getClassDetailsUpdateOperation(data)
        elif data["op"] == "d":
            pass
            # print("--------delete----------", data)
        else:
            # print("------------->:", data)
            exit()

    elif tableName == "ClassSummary" :
        if data["op"] == "d":
            pass
            # print ("--------deleted----------",data)
        elif data["op"] == "i":
            pass
            # print ("--------insert----------",data)
            getClassSummaryNum(data)
        elif data["op"] == "u":
            pass
            # print ("--------updated----------",data)
            exit()
        else:
            print("------------->:",data)
            exit()
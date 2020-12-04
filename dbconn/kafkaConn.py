
# import json
#
# from kafka import KafkaConsumer
#
# consumer = KafkaConsumer('mongodb-tes', bootstrap_servers=['10.0.0.64:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')))
# for message in consumer:
#     print ("%s:%d:%d: key=%s value=%s"%(message.topic, message.partition, message.offset, message.key, message.value))
#



import json
import conf
from kafka import KafkaConsumer

Options = None
isQuit = False
process_ctrls = []

def kafka_consumer_process():
    consumer = KafkaConsumer(bootstrap_servers=conf.KAFKA_BROKERS, group_id=Options.group_id or "php-group",
                             enable_auto_commit=False, value_deserializer=lambda x: json.loads(x.decode('ascii')))

    if Options.topics:
        topics = Options.topics.split(',')
    else:
        topics = "php-topic"
    consumer.subscribe(topics)

    # db = myMongo.myMongoClient()
    # try:
    #     while not isQuit:
    #         msg_pack = consumer.poll(timeout_ms=100)
    #         for tp, messages in msg_pack.items():
    #             for message in messages:
    #                 handle_php(db, message)
    #         consumer.commit_async()
    # except Exception as e:
    #     print("kafka_consumer_process exception: %s", str(e))
    # finally:
    #     consumer.commit()
    #     consumer.close()
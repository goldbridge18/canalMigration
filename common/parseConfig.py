
from configparser import ConfigParser
from common.setting import basePath

cfg = ConfigParser()
cfg.read("{basePath}/conf/setting.cnf".format(basePath=basePath))


#mysql info

ipaddr = cfg.get('mysqlInfo','ipaddr')
userName = cfg.get('mysqlInfo','userName')
password = cfg.get('mysqlInfo','password')
targetDatabaseName = cfg.get('mysqlInfo','databaseName')
port = cfg.getint('mysqlInfo','port')

#
databaseName = cfg.get('databaseInfo','databaseName')
tableName = cfg.get('databaseInfo','tableName')
fieldName = cfg.get('databaseInfo','fieldName')
jsonType = cfg.get('databaseInfo','jsonType')

#canal

client_id = bytes("{client_id}".format(client_id=cfg.getint('canalInfo','client_id')).encode("utf8"))
destination = bytes("{destination}".format(destination=cfg.get('canalInfo','destination')).encode("utf8"))

#获取指定的数据量
batchSize = cfg.getint('canalInfo','batchSize')


#kafka
groupId = cfg.get('kafkaInfo','groupId')
bootstrapServers=cfg.get('kafkaInfo','bootstrapServers')
topic=cfg.get('kafkaInfo','topic')
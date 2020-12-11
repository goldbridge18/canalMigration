import os,sys
import time,subprocess
import concurrent.futures
from impala.dbapi import connect

pathFile = "json"
dataxPath = "/data/datax/datax/bin"

def createJsonFile(pathFile):

    cmdList = []
    for i in range(1819):
        tableName = "ClusterMember_%05d"%i
        jsonStr = {
            "job": {"setting": {"speed": {"channel": 3, "byte": 1048576}, "errorLimit": {"record": 0, "percentage": 0.02}},
                    "content": [{"reader": {"name": "mysqlreader",
                                            "parameter": {"username": "datax", "password": "datax123", "splitPk": "",
                                                          "connection": [{"querySql": ["select * from %s;"%tableName],
                                                                          "jdbcUrl": [
                                                                              "jdbc:mysql://10.1.42.6:61106/eo_userinfo?serverTimezone=GMT%2B8"]}]}},
                                 "writer": {"name": "hdfswriter",
                                            "parameter": {"defaultFS": "hdfs://eeo-gic1-bj-zi-idc20-dhd112:8020",
                                                          "fileType": "text",
                                                          "path": "/user/hive/warehouse/eo_hadoop.db/ods_eeo_cluster_member",
                                                          "fileName": "ods_eeo_cluster_member", "writeMode": "append",
                                                          "fieldDelimiter": "\u0001",
                                                          "column": [{"name": "aid", "type": "bigint"},
                                                                     {"name": "clusterid", "type": "bigint"},
                                                                     {"name": "type", "type": "bigint"},
                                                                     {"name": "uid", "type": "bigint"},
                                                                     {"name": "status", "type": "bigint"},
                                                                     {"name": "cardsetting", "type": "bigint"},
                                                                     {"name": "cardinfover", "type": "bigint"},
                                                                     {"name": "nickname", "type": "string"},
                                                                     {"name": "identity", "type": "bigint"},
                                                                     {"name": "classidentity", "type": "bigint"},
                                                                     {"name": "gender", "type": "bigint"},
                                                                     {"name": "tel", "type": "varchar"},
                                                                     {"name": "email", "type": "varchar"},
                                                                     {"name": "comment", "type": "varchar"},
                                                                     {"name": "membersettingflags", "type": "bigint"},
                                                                     {"name": "allowspeaktime", "type": "bigint"},
                                                                     {"name": "exitmsgid", "type": "bigint"},
                                                                     {"name": "exitdisplayablemsgid", "type": "bigint"},
                                                                     {"name": "timetag", "type": "bigint"},
                                                                     {"name": "updatetime", "type": "string"}]}}}]}}

        jsonFilepath = "{path}/{tablename}.json".format(path=pathFile,tablename = tableName)

        if not os.path.isdir(pathFile):
            os.makedirs(pathFile)
        if os.path.isfile(jsonFilepath):
            os.remove(jsonFilepath)

        with open(jsonFilepath,"a+",encoding="utf8") as f:
            f.write(str(jsonStr))

        shellCmd = 'python  {dataxpath}/datax.py   -j "-Xms2G -Xmx2G"  {filePath}'.format(dataxpath = dataxPath,filePath = jsonFilepath)
        cmdList.append(shellCmd)
    return  cmdList


def connImpalaEexcCmd(cmd):
    db = connect(host='10.1.61.12', port=10000, database='eo_hadoop', auth_mechanism='PLAIN', user='hive')
    cursor = db.cursor()
    cursor.execute(cmd)




def run(cmd):

    stats, data = subprocess.getstatusoutput(cmd)
    if stats != 0:
        print("执行后返回状态（1表示失败，0表示成功）：",stats," ",cmd)


def concurExecCmd(strList):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futureToCmd = {executor.submit(run, sql): sql for sql in strList}
        for future in concurrent.futures.as_completed(futureToCmd):

            res = futureToCmd[future]


if __name__ == "__main__":

    #清除hadoop的数据
    hiveSql = "truncate table ods_eeo_cluster_member"
    connImpalaEexcCmd(hiveSql)
    #抽取数据
    concurExecCmd(createJsonFile(pathFile))

# from datetime import datetime, timedelta
# import os
# from impala.dbapi import connect
# db = connect(host='10.1.61.12', port=10000, database='eo_hadoop', auth_mechanism='PLAIN', user='hive')
# tablelist=["ods_eeo_login_user_classroom","ods_eeo_login_user"]
# cursor=db.cursor()
# b=datetime.today()-timedelta(days=1)
# c=b.strftime("%Y%m%d")
#
# datax_home_bin="/data/datax/datax/bin/"
# sql = """alter table {tablex} add  partition(dt="{run_date}") """
# shell='python datax.py  -j "-Xms2G -Xmx2G" -p "-Dpartition=dt={run_date} -Dct={run_date}" /root/yaoli/bak/datax.json.{tablex}'
#

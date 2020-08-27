import pymysql
import concurrent.futures
import urllib.request
import datetime


from common.parseConfig import *
from common.loggerout import writeLogContext
# mysql 执行sql语句



def execCmd(query,data = ""):
    '''
    insert/update command
    :param query:
    :return:

    host=None, user=None, password="",
                 database=None, port=0
    '''
    dateCur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = pymysql.connect(host= ipaddr, user= userName, password = password, database = targetDatabaseName, port = port)
    try:
        cursor = conn.cursor()
        if isinstance(query,list):
            for sql in query:
                sql = sql.replace("\'NULL\'","NULL")
                cursor.execute(sql)
        else:
            cursor.execute(query)
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        writeLogContext(e,"info")
        writeLogContext(data,"info")
        writeLogContext(query,"info")
    conn.close()
#多线程执行.(出现重复插入的情况，待解决)
def concurExecSql(strList):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Start the load operations and mark each future with its URL
        future_to_sql = {executor.submit(execCmd, sql): sql for sql in strList}
        for future in concurrent.futures.as_completed(future_to_sql):
            sql = future_to_sql[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (sql, exc))
            else:
                for i in strList:
                    execCmd(i)
                    with open("./sql/insert_sql.sql", "a+", encoding="utf8") as f:
                        f.write("\n")
                        f.write(i)
                    # print("insert1 :", i)
                print('%r  is succeed !' % (sql))



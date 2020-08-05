import pymysql
import concurrent.futures
import urllib.request
import datetime


from common.parseConfig import *
# mysql 执行sql语句



def execCmd(query):
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
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        conn.rollback()
        with open("./logs/err_sql.log", "a+", encoding="utf8") as f:
            f.write("\n")
            f.write("{date}-->{i}: ".format(date = dateCur,i = query))

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



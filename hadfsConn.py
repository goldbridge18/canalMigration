from hdfs.client import Client


# 获取HDFS连接
def getHDFSConn():
    client = None
    try:
        client = Client("http://20.58.32.8:50070", root='/')
    except Exception as e:
        print(e)
    return client


# 创建目录
def mkdirs(client, hdfs_path):
    client.makedirs(hdfs_path)


# 上传本地文件到hdfs
def putLocalFileToHDFS(client, hdfs_path, local_path):
    client.upload(hdfs_path, local_path, cleanup=True)


# 数据写入到初次创建文件或者覆盖文件
def writeToHDFS(client, hdfs_path, data):
    client.write(hdfs_path, data, overwrite=True, append=False, encoding='utf-8')


# 追加数据到hdfs文件
def appendWriteToHDFS(client, hdfs_path, data):
    client.write(hdfs_path, data, overwrite=False, append=True, encoding='utf-8')


# DF写入到初次创建文件或者覆盖文件
def writeDFtoHDFS(client, hdfs_path, df):
    client.write(hdfs_path, df.to_csv(index=False, header=False, sep=','), encoding='utf-8', overwrite=True,
                 append=False)


# 追加DF数据到hdfs文件
def appendWriteDFtoHDFS(client, hdfs_path, df):
    client.write(hdfs_path, df.to_csv(index=False, header=False, sep=','), encoding='utf-8', overwrite=False,
                 append=True)


# 删除hdfs文件
# 删除文件夹,该文件夹必须为空
def deleteHDFSfile(client, hdfs_path):
    client.delete(hdfs_path)


# 修改文件夹或者文件名称
def moveOrRename(client, hdfs_src_path, hdfs_dst_path):
    client.rename(hdfs_src_path, hdfs_dst_path)


# 获取文件夹下的文件
def getFileList(client, hdfs_path):
    return client.list(hdfs_path, status=False)


# 下载hdfs文件到本地
def getFileFromHDFS(client, local_path, hdfs_path):
    client.download(hdfs_path, local_path, overwrite=False)


# 读取文件信息
def readHDFSfile(client, filename):
    lines = []
    with client.read(filename, encoding='utf-8', delimiter='\n') as reader:
        for line in reader:
            lines.append(line.strip())
    return lines
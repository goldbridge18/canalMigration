import logging
import os

basePath = os.path.dirname(os.path.dirname(__file__))
logfilepath = "{path}/logs/info.log".format(path = basePath)
print(logfilepath)
def writeLogContext(context,modlename):

    #创建logger记录器
    logger = logging.getLogger(modlename)
    logger.setLevel(logging.DEBUG)

    #日志保存到磁盘文件的处理器
    fh = logging.FileHandler(logfilepath,encoding='utf8')
    fh.setLevel(logging.DEBUG)
    ''' 
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    #sh.setFormatter(formatter)

    logger.addHandler(fh)
    #logger.addHandler(sh)

    logger.debug(context)



# log = 'debug.共产党'

# modlename = 'info'
# writeLogContext(log,modlename)
 
import logging
import os

def writeLogContext(context,modlename,logfilepath):

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


''' 
log = 'debug.共产党'
path = ''
modlename = ''
writeLogContext(log,os.path.basename(__file__),'debug.log')
 '''
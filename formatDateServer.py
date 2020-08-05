import datetime,time



def formatDate(timeStamp):
    if len(str(timeStamp)) == 13:
        cutTimeStamp = int(round(timeStamp/1000))
        formatLocal = time.localtime(cutTimeStamp)
        formatAfterTime = time.strftime("%Y-%m-%d %H:%M:%S", formatLocal)
        # print(formatAfterTime)
    elif len(str(timeStamp)) == 10:

        formatLocal = time.localtime(timeStamp)
        formatAfterTime = time.strftime("%Y-%m-%d %H:%M:%S", formatLocal)

    return formatAfterTime
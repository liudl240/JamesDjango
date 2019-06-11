import time


def initTime(): 
    # 格式化成2016-03-20 11:45:39形式
    des_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return des_time



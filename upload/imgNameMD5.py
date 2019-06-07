import hashlib
import time
import random
import re
input_ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def imgNameMD5(input_imgname):      #加盐，盐的默认值是空
    salt=str(random.random())
    string = input_ctime
    string=string+salt
    news=str(string).encode()
    m=hashlib.md5(news)
    imgtype=input_imgname.split(".")[1]
    imgname="{_imgname}.{_imgtype}".format(_imgname=m.hexdigest(),_imgtype=imgtype)
    return imgname

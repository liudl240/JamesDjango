import hashlib
import time
import random
import re
input_ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def NameMD5():      #加盐，盐的默认值是空
    salt=str(random.random())
    string = input_ctime
    string=string+salt
    news=str(string).encode()
    m=hashlib.md5(news)
    name="{_imgname}.md".format(_imgname=m.hexdigest())
    return name


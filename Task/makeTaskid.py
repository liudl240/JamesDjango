import hashlib

def taskidMD5(string):
    hash=hashlib.md5()
    hash.update(string.encode('utf-8'))
    res=hash.hexdigest()
    return res
    
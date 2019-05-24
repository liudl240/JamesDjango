import random
 
def emailcode():
    source = "0123456789"
    code_str = ""
    for i in range(4):
        tmp_num = random.randrange(len(source))
        random_str = source[tmp_num]
        code_str += random_str
    return code_str

import hashlib
import random
from django.forms.models import model_to_dict
# from Task.models import tasks

def taskidMD5(string):
    hash=hashlib.md5()
    hash.update(string.encode('utf-8'))
    res=hash.hexdigest()
    return res

def tagcolor():
    color_list= [
        # "label-default",
        "label-primary",
        "label-success",
        "label-info",
        "label-warning",                
        "label-danger",
        "label-dark",
        # "label-secondary",
        "label-purple",
        "label-pink",
        "label-cyan",
        "label-yellow",
        "label-brown"
    ]
    ret = random.choice(color_list)
    return ret

def tag_tagcolor(taskinfolist):
    """转化为json"""
    tasklist_json = []
    for tasklist in taskinfolist:
        """修改枚举值"""
        tasklist.status = tasklist.get_status_display()
        tasklist.tasktype = tasklist.get_tasktype_display()
        json_dict = model_to_dict(tasklist)
        tasklist_json.append(json_dict)
    for taglist in tasklist_json:
        """转化为列表组合，[[tag,color],[tag2,color2]]"""
        taglists= []
        for tag in taglist["tags"].split(","):
            taglists.append([tag,tagcolor()])
        taglist["tags"]= taglists
    return tasklist_json

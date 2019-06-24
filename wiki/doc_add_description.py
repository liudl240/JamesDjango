from django.forms.models import model_to_dict
from JamesDjango.settings import MEDIA_ROOT

def doc_add_description(docinfolist):
    """转化为json"""
    docinfo_json = []
    for docinfo in docinfolist:
        """添加为何创建文档"""
        docinfo.description ="abc123"
        json_dict = model_to_dict(docinfo)
        docinfo_json.append(json_dict)
    for docinfo in docinfo_json:
        with open("{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname=docinfo["content"]),"r", encoding="utf-8") as f:
             description=""
             for line in  f.readlines():
                 if line[0] == "#":
                     description = description + line
                 if line[0] == ">": 
                     description = description + line
        docinfo["description"] = description
        print(docinfo["description"])
    return docinfo_json 

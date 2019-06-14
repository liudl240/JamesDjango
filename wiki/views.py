from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from JamesDjango.settings import MEDIA_ROOT
from Task.models import tasks
from wiki.models import doc
from Users.models import UserInfo
from wiki.docname import NameMD5
from Users.initTime import initTime
import markdown

# Create your views here.

"""文章列表"""
def wikilist(request):
    doc_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname="abc.html")
    return render(request, "abc.html")

"""任务列表，点击解决文档的时候执行"""
def Solve_doc(request):
    """获取任务ID"""
    task_id = request.GET.get("task_id",None)
    taskinfo = tasks.objects.all().filter(id=task_id)[0]

    """用户信息"""
    username = request.session.get("username",None)
    userinfo =  UserInfo.objects.all().filter(username=username)[0] 
    """如何存在任务文档直接返回，反则创建新的文档"""
    if taskinfo.doc_id == None:
        """标题等于任务名称"""
        title = taskinfo.title
        """markdown文件名字"""
        new_md_name = NameMD5()
        with open("{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname=new_md_name), "w") as f:
            f.write("# 请开始你的表演")
            f.close()
        """写入数据库"""
        new_doc = doc(
            title = title ,
            c_time = initTime(),
            content = new_md_name,
        )
        new_doc.save()
        """更新文档ID到任务表"""
        tasks.objects.filter(id=task_id).update(doc_id=new_doc.id)
        docinfo = doc.objects.all().filter(id=new_doc.id)
        content = {"docinfo":docinfo}
        return render(request, "wiki/adddoc.html",content) 
    else:
        doc_id = taskinfo.doc_id
        docinfo = doc.objects.all().filter(id=doc_id)
        html = "wiki/doc/{}.html".format(docinfo[0].content.split(".md")[0])
        return render(request,html) 
    return render(request, "wiki/adddoc.html",content) 

""""""
def savedoc(request):
    doc_id = request.GET.get("doc_id",None) 
    if request.method == "POST":
        docinfo = doc.objects.all().filter(id=doc_id)
        #获取titile
        title = request.POST.get("title",None)
        print(title)
        #markdown
        doc_markdown = request.POST.get("test-editormd-markdown-doc",None)
        #html
        doc_html = request.POST.get("test-editormd-html-code",None)
        #文件名
        doc_name = docinfo[0].content.split(".md")[0]
        doc_markdown_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname=doc_name)
        with open("{}.md".format(doc_markdown_name), 'w') as f :
            f.close()
        with open("./templates/wiki/doc/{}.html".format(doc_name),'w') as f:
            f.write(doc_html)
            f.close()
        docinfo.update(title=title)
    return HttpResponseRedirect('/task/tasklist')

 
"""添加文章"""
def adddoc(request):
    username = request.session.get("username",None)
    userinfo = UserInfo.objects.all().filter(username=username)

    taskid = request.GET.get("task")
    if request.method == "POST":
        #获取titile
        title = request.POST.get("title",None)
        print(title)
        #markdown
        doc_markdown = request.POST.get("test-editormd-markdown-doc",None)
        #html
        doc_html = request.POST.get("test-editormd-html-code",None)
        #文件名
        doc_markdown_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname="abc")
        #doc_html_name = 
        with open("{}.md".format(doc_markdown_name), 'w') as f :
            f.write(doc_markdown)  
            f.close()
        with open("{}.html".format("./templates/abc"),'w') as f:
            f.write(doc_html)  
            f.close()
        return HttpResponseRedirect('/wiki/adddoc.html')
    return render(request, "wiki/adddoc.html")



"""删除文章"""
def deldoc(request):
    pass






"""编辑文档"""
def editdoc(request):
    pass

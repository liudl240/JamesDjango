from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from JamesDjango.settings import MEDIA_ROOT
from Task.models import tasks
from wiki.models import doc
from Users.models import UserInfo
from wiki.docname import NameMD5
from wiki.doc_add_description import doc_add_description
from Users.initTime import initTime
from Users.views import login_require
import markdown
from Task.makeTaskid import taskidMD5,tag_tagcolor
from django.utils.html import strip_tags
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage
# Create your views here.

"""文章列表"""
@login_require
def wikilist(request):
    doc_info = doc.objects.all()
    """搜索"""
    key_world=request.GET.get("search",None) 
    if key_world != None:
        doc_info = doc.objects.all().filter(title__icontains=key_world)
    """显示task中为何创建"""
    doc_info = doc_add_description(doc_info)
    """"分页"""
    # 值1：所有的数据
    # 值2：每一页的数据
    # 值3：当最后一页数据少于n条，将数据并入上一页
    paginator = Paginator(doc_info,4,1)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index','1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)
    content = {'page':number,'paginator':paginator} 
    return render(request, 'wiki/doclist.html',content)

"""任务列表，点击解决文档的时候执行"""
@login_require
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
        with open("{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname=new_md_name), "w",encoding='utf-8') as f:
            f.write("# 请开始你的表演")
            f.close()
        """写入数据库"""
        new_doc = doc(
            title = title ,
            c_time = initTime(),
            content = new_md_name,
            username_id = username,
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
        # 获取tag
        taskinfo = tasks.objects.all().filter(id=taskinfo.id)
        taskinfo = tag_tagcolor(taskinfo)
        content = {"docinfo": docinfo,"taskinfo":taskinfo[0]}
        return render(request,'wiki/showdoc.html',content) 
    return render(request, "wiki/adddoc.html",content) 

"""保存文档"""
@login_require
def savedoc(request):
    doc_id = request.GET.get("doc_id",None) 
    if request.method == "POST":
        docinfo = doc.objects.all().filter(id=doc_id)
        #获取titile
        title = request.POST.get("title",None)
        #markdown
        doc_markdown = request.POST.get("test-editormd-markdown-doc",None)
        # 文件名
        doc_name = docinfo[0].content
        doc_markdown_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname=doc_name)
        # 写入文件
        with open("{}".format(doc_markdown_name), 'w',encoding='utf-8') as f :
            f.write(doc_markdown)
            f.close()
        docinfo.update(title=title)
    return HttpResponseRedirect('/task/tasklist')

 
"""添加文章"""
#@login_require
#def adddoc(request):
#    username = request.session.get("username",None)
#    userinfo = UserInfo.objects.all().filter(username=username)
#
#    taskid = request.GET.get("task")
#    if request.method == "POST":
#        #获取titile
#        title = request.POST.get("title",None)
#        print(title)
#        #markdown
#        doc_markdown = request.POST.get("test-editormd-markdown-doc",None)
#        #html
#        doc_html = request.POST.get("test-editormd-html-code",None)
#        #文件名
#        doc_markdown_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname="abc")
#        #doc_html_name = 
#        with open("{}.md".format(doc_markdown_name), 'w') as f :
#            f.write(doc_markdown)  
#            f.close()
#        return HttpResponseRedirect('/wiki/adddoc.html')
#    return render(request, "wiki/adddoc.html")



"""删除文章"""
@login_require
def deldoc(request):
    pass


"""查看文章"""
@login_require
def showdoc(request):
    doc_id = request.GET.get("doc_id",None)
    docinfo = doc.objects.all().filter(id=doc_id)
    # 获取tag
    taskinfo = tasks.objects.all().filter(doc_id=doc_id) 
    if len(taskinfo) > 0:
        taskinfo = tag_tagcolor(taskinfo)[0]
    else:
        taskinfo=None
    content = {"docinfo": docinfo,"taskinfo":taskinfo}
    return render(request,'wiki/showdoc.html',content)



"""编辑文档"""
@login_require
def editdoc(request):
    doc_id = request.GET.get("id",None) 
    if doc_id != None:
        docinfo =  doc.objects.all().filter(id=doc_id)
        content = {"docinfo":docinfo}
    else:
        return HttpResponse("文章不存在，不能编辑")
    return render(request, "wiki/adddoc.html",content) 
"""上传图片"""
@login_require
def wikiimg(request):
    if request.method == "POST":
        img = request.FILES.get('fileName',None)
        if img != None:
            status="success"
    return HttpResponse({success:1,message:"提示的信息，上传成功或上传失败及错误信息等。",url:"http://www.baidu.com"})

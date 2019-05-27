from django.shortcuts import render, render_to_response
from Users.views import login_require
from mysites import models
"""主页"""
@login_require
def index(request):
    username = request.session.get("username", None)
    if username == None:
        return render(request,"Users/login.html")
    else:
        context = {"username":username}
        return render(request, 'index.html',context)


"""生产链接"""
@login_require
def servicelist(request):
    username = request.session.get("username", None)
    servicelistinfo = models.servicelist.objects.all()
    context = {"username":username,"servicelistinfo":servicelistinfo}
    if request.method == "POST":
        input_title = request.POST.get("title",None)
        input_jumpLink = request.POST.get("jumpLink",None)
        input_desLink = request.POST.get("desLink",None)
        print(input_title,input_jumpLink,input_desLink)
        titleinfo = models.servicelist.objects.filter(title=input_title)
        jumpLinkinfo = models.servicelist.objects.filter(jumpLink=input_jumpLink)
        if input_title == "" or  input_jumpLink == "":
            status="请认证填写，不能为空"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo}
            return render(request, 'service/servicelist.html',context)
        elif len(titleinfo) > 0 or len(jumpLinkinfo) > 0:
            status="连接获取标题已存在，请查阅后添加"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo}
            return render(request, 'service/servicelist.html',context)
        else:
            models.servicelist.objects.create(title=input_title,jumpLink=input_jumpLink,desLink=input_desLink)
            status="提交成功"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo}
            return render(request, 'service/servicelist.html',context)
    return render(request, 'service/servicelist.html',context)

"""编辑链接"""
def editservice(request):
    username = request.session.get("username", None)
    servicelistinfo = models.servicelist.objects.all()
    edit_title = request.GET.get("title",None)
    print("编辑标题："+edit_title)
    serviceinfo = models.servicelist.objects.filter(title=edit_title) 
    context = {"username":username,"servicelistinfo":servicelistinfo,"serviceinfo":serviceinfo}
    if request.method == "POST":
        input_title = request.POST.get("title",None)
        input_jumpLink = request.POST.get("jumpLink",None)
        input_desLink = request.POST.get("desLink",None)
        print(input_title,input_jumpLink,input_desLink)
        titleinfo = models.servicelist.objects.filter(title=input_title)
        jumpLinkinfo = models.servicelist.objects.filter(jumpLink=input_jumpLink)
        if input_title == "" or  input_jumpLink == "":
            status="请认证填写，不能为空"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo}
            return render(request, 'service/servicelist.html',context)
        elif len(titleinfo) > 0 or len(jumpLinkinfo) > 0:
            status="连接获取标题已存在，请查阅后添加"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo}
            return render(request, 'service/servicelist.html',context)
        else:
            models.servicelist.objects.create(title=input_title,jumpLink=input_jumpLink,desLink=input_desLink)
            status="提交成功"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo}
            return render(request, 'service/servicelist.html',context)
    return render(request, 'service/editservice.html',context)


"""404页面"""
def page_not_found(request):
    return render_to_response('404.html')

"""500页面"""
def page_error(request):
    return render_to_response('500.html')

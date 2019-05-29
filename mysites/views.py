from django.shortcuts import render, render_to_response,HttpResponseRedirect,redirect
from Users.views import login_require
import random
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
    color=random.choice(['bg-success','bg-warning','bg-danger','bg-purple','bg-cyan','bg-brown','bg-info','bg-primary'])
    color ="\"card-header {_color}\"".format(_color=color)
    print(color)
    username = request.session.get("username", None)
    servicelistinfo = models.servicelist.objects.all()
    context = {"username":username,"servicelistinfo":servicelistinfo,"color":color }
    if request.method == "POST":
        input_title = request.POST.get("title",None)
        input_jumpLink = request.POST.get("jumpLink",None)
        input_desLink = request.POST.get("desLink",None)
        titleinfo = models.servicelist.objects.filter(title=input_title)
        jumpLinkinfo = models.servicelist.objects.filter(jumpLink=input_jumpLink)
        print(input_title,input_jumpLink,input_desLink)
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
    edit_id = request.GET.get("id",None)
    print(edit_id)
    idinfo = models.servicelist.objects.filter(id=edit_id)
    if len(idinfo) == 0:
        status = "没有如此的id号"
        context = {"username":username,"servicelistinfo":servicelistinfo,"error_msg":status}
        return render(request, 'service/servicelist.html',context)
    context = {"username":username,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
    if request.method == "POST":
        input_title = request.POST.get("title",None)
        input_jumpLink = request.POST.get("jumpLink",None)
        input_desLink = request.POST.get("desLink",None)
        edit_id = request.GET.get("id",None)
        idinfo = models.servicelist.objects.filter(id=edit_id)
        print(input_title,input_jumpLink,input_desLink+"JAMES TEST",edit_id)
        titleinfo = models.servicelist.objects.filter(title=input_title)
        jumpLinkinfo = models.servicelist.objects.filter(jumpLink=input_jumpLink)
        idinfo = models.servicelist.objects.filter(id=edit_id)
        print("testjames001")
        if input_desLink =="" and input_jumpLink == "" and input_title == "":
            status = "没有修改编辑，不能都为空"
            context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
            return render(request, 'service/editservice.html',context)
        elif input_title != "" or input_jumpLink != "":
            if len(titleinfo) > 0 or len(jumpLinkinfo) > 0:
                status="连接获取标题已存在，请查阅后添加"
                context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
                return render(request, 'service/editservice.html',context)
        if input_title != "":
            idinfo.update(title = input_title)
        elif input_jumpLink != "":
            idinfo.update(jumpLink=input_jumpLink)
        elif input_desLink != "":
            idinfo.update(desLink=input_desLink)
        status="提交成功"
        context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
        return render(request, 'service/editservice.html',context)


        # if input_title == "" or  input_jumpLink == "":
        #     status="请认证填写，不能为空"
        #     context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
        #     return render(request, 'service/editservice.html',context)
        # elif input_title == titleinfo[0].title or input_jumpLink == jumpLinkinfo[0].jumpLink:
        #     idinfo.update(title=input_title,jumpLink=input_jumpLink,desLink=input_desLink)
        #     status="提交成功"


        
        #     context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
        #     return render(request, 'service/editservice.html',context)
        # elif len(titleinfo) > 0 or len(jumpLinkinfo) > 0:
        #     status="连接获取标题已存在，请查阅后添加"
        #     context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
        #     return render(request, 'service/editservice.html',context)
        # else:
        #     idinfo.update(title=input_title,jumpLink=input_jumpLink,desLink=input_desLink)
        #     status="提交成功"
        #     context= {"username":username, "error_msg":status,"servicelistinfo":servicelistinfo,"idinfo":idinfo[0]}
        #     return render(request, 'service/editservice.html',context)
    return render(request, 'service/editservice.html',context)

"""删除链接"""
@login_require
def delservice(request):
    edit_id = request.GET.get("id", None)
    idinfo = models.servicelist.objects.filter(id=edit_id)
    servicelistinfo = models.servicelist.objects.all()
    username = request.session.get("username", None)

    if len(idinfo) == 0 :
        context = {"error_msg": "没有这个id","username":username}
        return HttpResponseRedirect( 'service/servicelist.html', context)
    idinfo.delete()
    context = {"error_msg":"删除成功","servicelistinfo":servicelistinfo,"username":username}
    return render(request,'service/servicelist.html',context)

"""404页面"""
def page_not_found(request):
    return render_to_response('404.html')

"""500页面"""
def page_error(request):
    return render_to_response('500.html')

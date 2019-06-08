from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from datetime import *
import time
from Task.models import tasks
from Task.models import task_point
from upload.models import IMG
from Task.makeTaskid import taskidMD5,tag_tagcolor
from Task.choices_switch import choices_switch
from Users.views import login_require
import json


# Create your views here.


    
@login_require
def tasklist(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    input_title = request.POST.get('title') 
    input_username = request.POST.get('username') 
    input_status = request.POST.get('status') 
    input_search_field = None
    input_keyword = None
    # print(input_title,input_username,input_status)
    if request.method == "POST":
        input_search_field = request.POST.get("search_field")
        input_keyword = request.POST.get("keyword",None)
        print(input_search_field,input_keyword)
        if input_keyword != None:
            """标题检索"""
            if input_search_field == "title":
                taskinfolist = tasks.objects.all().filter(title__icontains=input_keyword)
            """作者检索"""
            if input_search_field == "username":
                taskinfolist = tasks.objects.all().filter(username=input_keyword)
            """状态检索"""
            if input_search_field == "status":
                status_code = choices_switch("GENDER_CHOICES1",input_keyword)
                taskinfolist = tasks.objects.all().filter(status=status_code )  
            """类型检索"""
            if input_search_field == "tasktype":
                tasktype_code = choices_switch("GENDER_CHOICES",input_keyword)
                taskinfolist = tasks.objects.all().filter(tasktype=tasktype_code)

    tasklist_json = tag_tagcolor(taskinfolist)
    context = {"username":username,"tasklist_json":tasklist_json,"input_search_field":input_search_field,"input_keyword":input_keyword}
    return render(request,'task/tasklist.html',context)


@login_require
def taskinfo(request):
    username = request.session.get("username", None)
    input_task_id = request.GET.get("task_id",None)
    taskinfo = tasks.objects.all().filter(id=input_task_id)
    task_point_list = task_point.objects.filter(task_id=input_task_id)
    imglist = IMG.objects.all().filter(task_id=input_task_id)
    taglist = taskinfo[0].tags.split(",")
    # print(taglist)
    taskinfo = tag_tagcolor(taskinfo)
    # print(taskinfo[0])
    # context={"username":username,"taskinfo":taskinfo[0],"task_point_list":task_point_list,"imglist":imglist,"task_id":input_task_id,"taglist":taglist}
    context={"username":username,"taskinfo":taskinfo[0],"task_point_list":task_point_list,"imglist":imglist}
    return render(request,'task/taskinfo.html',context)
@login_require
def addtask(request):
    username = request.session.get("username", None)
    taskid = taskidMD5(username)
    request.session['taskidMD5'] = taskid
    imgs=IMG.objects.all()
    context = {"username":username,"imgs":imgs}
    print("*____________________"* 3)
    if request.method == "POST":
        """输入"""
        input_tasktype = request.POST.get("type",None)
        input_title = request.POST.get("title",None)
        input_description = request.POST.get("description",None)
        input_tags = request.POST.get("tags",None)
        input_status = request.POST.get("status",None)
        """需要添加"""
        input_ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        new_task = tasks(
            username_id=username,
            title = input_title,
            tasktype = input_tasktype,
            tags = input_tags,
            c_time = input_ctime,
            status = input_status, 
            description = input_description,
        ) 
        new_task.save()
        # print("新任务的ID号："+ str(new_task.id))
        IMG.objects.filter(active=taskid).update(task_id=new_task.id,active=None)         
        # print(input_tasktype,input_title,input_description,input_tags,input_status)
        return HttpResponseRedirect('task/tasklist.html',context)
    return render(request,'task/addtask.html',context)
@login_require
def edittask(request):
    input_task_id = request.GET.get("task_id",None)
    username = request.session.get("username", None)
    taskid = taskidMD5(username)
    request.session['taskidMD5'] = taskid
    taskinfo = tasks.objects.all().filter(id=input_task_id)
    imglist = IMG.objects.all().filter(task_id=input_task_id)
    context = {"username":username,"taskinfo":taskinfo[0],"imglist":imglist,"task_id":input_task_id}
    if input_task_id != None:
        if request.method == "POST":
            taskinfolist = tasks.objects.all()
            context = {"username":username,"taskinfolist":taskinfolist}
            input_tasktype = request.POST.get("type",None)
            input_title = request.POST.get("title",None)
            input_description = request.POST.get("description",None)
            input_tags = request.POST.get("tags",None)
            input_status = request.POST.get("status",None)
            input_task_id = request.GET.get("task_id",None)
            if input_task_id != None:
                taskinfo.update(title=input_title,tasktype=input_tasktype,tags=input_tags,status=input_status,description=input_description)
                IMG.objects.filter(active=taskid).update(task_id=input_task_id,active=None)  
            return HttpResponseRedirect('/task/tasklist.html',context)
        return render(request,'task/edittask.html',context )
    else:
        return HttpResponse("没有如此ID")
        
@login_require
def deltask(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    """获取复选框内容"""
    check_box_list = request.GET.getlist('ids[]')
    """获取id对象"""
    for input_task_id in check_box_list:
        """获取id的对象"""
        taskinfo = tasks.objects.filter(id=input_task_id)
        """移除task"""
        taskinfo.delete()
    context = {"username":username,"taskinfolist":taskinfolist}
    return HttpResponseRedirect('/task/tasklist.html',context)
@login_require
def starttask(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    """获取复选框值"""
    check_box_list = request.GET.getlist('ids[]')
    print(check_box_list)
    """点击启动，如何启动时间为None则修改启动时间，修改task状态"""
    for input_task_id in check_box_list:
        """获取id的对象"""
        taskinfo = tasks.objects.filter(id=input_task_id)
        """只有状态是未启动【0】的时候才会启动"""
        if taskinfo[0].status == 0:
            taskinfo.update(status=1)
        """修改启动时间"""
        if taskinfo[0].s_time == None:
            input_stime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            taskinfo.update(s_time=input_stime)
    context = {"username":username,"taskinfolist":taskinfolist}
    return HttpResponseRedirect('/task/tasklist.html',context)
@login_require
def complatetask(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    context = {"username":username,"taskinfolist":taskinfolist}
    """获取复选框值"""
    check_box_list = request.GET.getlist('ids[]')
    # print(check_box_list)
    """获取taskid对象"""
    for input_task_id in check_box_list:
        """获取对象"""
        taskinfo = tasks.objects.filter(id=input_task_id)
        """只有状态为进行中的时候才可以修改状态"""
        """修改完成时间"""
        if taskinfo[0].status == 1:
            input_ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            taskinfo.update(status=2,f_time=input_ftime)
    return HttpResponseRedirect('/task/tasklist.html',context)
@login_require
def add_task_point(request):
    input_task_id = request.GET.get("task_id",None)
    username = request.session.get("username", None)
    #context = {"username":username}
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    context = {"username":username,"task_point_info":task_point_info,"task_id":input_task_id}
    if input_task_id != None:
        context = {"username":username,"task_point_info":task_point_info,"task_id":input_task_id}
        if request.method == "POST":
            print("开始提交表达")
            input_ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            input_status = request.POST.get("type",None)
            input_title = request.POST.get("title",None) 
            if input_title != None:
                new_task_point = task_point(
                    title = input_title,
                    c_time = input_ctime,
                    status = input_status,
                    task_id = input_task_id
                )
                new_task_point.save()
    else:
        print("没有如此ID")
        context = {"username":username,"task_point_info":task_point_info,"status":"没有如此ID","task_id":None}
        return render(request,'task/add_task_point.html',context)
    return render(request,'task/add_task_point.html',context)
@login_require
def del_task_point(request):
    print("到这里了") 
    username = request.session.get("username", None)
    input_task_id = request.GET.get("task_id",None)
    input_task_point_id = request.GET.get("task_point_id",None)
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    context = {"username":username,"task_point_info":task_point_info,"status":"没有如此ID"}
    task_point_info = task_point.objects.all().filter(id=input_task_point_id)    
    if len(task_point_info) == 1:
        task_point_info.delete()
    else:
        return HttpResponse("没有如此ID")
    return HttpResponseRedirect('/task/add_task_point/?task_id={}'.format(input_task_id))
@login_require
def edit_task_point(request):
    username = request.session.get("username", None)
    input_task_id = request.GET.get("task_id",None)
    input_task_point_id = request.GET.get("task_point_id",None)
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    task_point1 = task_point.objects.all().filter(id=input_task_point_id)
    context = {"username":username,"task_point_info":task_point_info,"task_id":input_task_id,"task_point1":task_point1[0]}
    print(task_point1[0].f_time)
    if request.method == "POST":
        input_f_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        input_title = request.POST.get("title",None)
        input_status = request.POST.get("type",None)
        task_point1.update(title=input_title,status=input_status)
        if input_status == "2":
            task_point1.update(f_time=input_f_time)
        else:
            task_point1.update(f_time=None)
    return render(request,'task/edit_task_point.html',context)

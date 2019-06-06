from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from datetime import *
import time
from Task.models import tasks
from Task.models import task_point
from upload.models import IMG

# Create your views here.

def tasklist(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    context = {"username":username,"taskinfolist":taskinfolist}
    input_title = request.POST.get('title') 
    input_username = request.POST.get('username') 
    input_status = request.POST.get('status') 
    print(input_title,input_username,input_status)
    return render(request,'task/tasklist.html',context)

def taskinfo(request):
    username = request.session.get("username", None)
    input_task_id = request.GET.get("task_id",None)
    input_task_id = request.GET.get("task_id",None)
    taskinfo = tasks.objects.all().filter(id=input_task_id)
    task_point_list = task_point.objects.filter(task_id=input_task_id)
    imglist = IMG.objects.all().filter(task_id=input_task_id)
    input_task_id = request.GET.get("task_id",None)
    context={"username":username,"taskinfo":taskinfo[0],"task_point_list":task_point_list,"imglist":imglist,"task_id":input_task_id}
    return render(request,'task/taskinfo.html',context)

def addtask(request):
    username = request.session.get("username", None)
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
        print(input_tasktype,input_title,input_description,input_tags,input_status)
        return HttpResponseRedirect('task/tasklist.html',context)
    return render(request,'task/addtask.html',context)

def edittask(request):
    input_task_id = request.GET.get("task_id",None)
    username = request.session.get("username", None)
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
            return HttpResponseRedirect('/task/tasklist.html',context)
        return render(request,'task/edittask.html',context )
    else:
        return HttpResponse("没有如此ID")
        

def deltask(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    context = {"username":username,"taskinfolist":taskinfolist}
    return HttpResponseRedirect('/task/tasklist.html',context)

def starttask(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    context = {"username":username,"taskinfolist":taskinfolist}
    return HttpResponseRedirect('/task/tasklist.html',context)

def complatetask(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    context = {"username":username,"taskinfolist":taskinfolist}
    #check_box_list = request.POST.getlist('checkbox')
    check_box_list = request.GET.getlist('checkbox')
    print(check_box_list)
    return HttpResponseRedirect('/task/tasklist.html',context)

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

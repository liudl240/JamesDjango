from django.shortcuts import render,HttpResponseRedirect
from datetime import *
import time
from Task.models import tasks
from upload.models import IMG

# Create your views here.

def tasklist(request):
    username = request.session.get("username", None)
    taskinfolist = tasks.objects.all()
    tagslist = taskinfolist[0].tags
    print(tagslist)
    context = {"username":username,"taskinfolist":taskinfolist,"tagslist":tagslist}
  
    return render(request,'task/tasklist.html',context)


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
        input_tags = request.POST.get("tags",None).split(",")
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
        return HttpResponseRedirect('task/addtask.html',context)
    return render(request,'task/addtask.html',context)

def edittask(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/edittask.html',context)

def deltask(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/deltask.html',context)


def add_task_point(request):
    pass
    return render(request,'task/add_task_point.html')

def del_task_point(request):
    pass
    return render(request,'task/del_task_point.html')

def edit_task_point(request):
    pass
    return render(request,'task/edit_task_point.html')

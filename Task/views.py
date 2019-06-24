from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from datetime import *
from Users.initTime import initTime
from Task.models import tasks
from Task.models import task_point
from upload.models import IMG
from Task.makeTaskid import taskidMD5,tag_tagcolor
from Task.choices_switch import choices_switch
from Users.views import login_require
from Users.models import UserInfo
import json,os 
from JamesDjango.settings import MEDIA_ROOT
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage
# Create your views here.


    
@login_require
def tasklist(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    taskinfolist = tasks.objects.all()
    input_title = request.POST.get('title') 
    input_username = request.POST.get('username') 
    input_status = request.POST.get('status') 
    input_search_field = "title"
    input_keyword = ""
    if request.method == "POST":
        input_search_field = request.POST.get("search_field")
        input_keyword = request.POST.get("keyword",None)
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

    """"分页"""
    # 值1：所有的数据
    # 值2：每一页的数据
    # 值3：当最后一页数据少于n条，将数据并入上一页
    paginator = Paginator(tasklist_json,10,3)
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

    context = {"userinfo":userinfo[0],"tasklist_json":tasklist_json,"input_search_field":input_search_field,"input_keyword":input_keyword, 'page':number,'paginator':paginator}
    return render(request,'task/tasklist.html',context)


@login_require
def taskinfo(request):
    username = request.session.get("username",None)
    userinfo = UserInfo.objects.filter(username=username)
    input_task_id = request.GET.get("task_id",None)
    taskinfo = tasks.objects.all().filter(id=input_task_id)
    task_point_list = task_point.objects.filter(task_id=input_task_id)
    imglist = IMG.objects.all().filter(task_id=input_task_id)
    taglist = taskinfo[0].tags.split(",")
    taskinfo = tag_tagcolor(taskinfo)
    # context={"username":username,"taskinfo":taskinfo[0],"task_point_list":task_point_list,"imglist":imglist,"task_id":input_task_id,"taglist":taglist}
    context={"userinfo":userinfo[0],"taskinfo":taskinfo[0],"task_point_list":task_point_list,"imglist":imglist}
    return render(request,'task/taskinfo.html',context)



@login_require
def addtask(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    taskid = taskidMD5(username)
    request.session['taskidMD5'] = taskid
    imgs=IMG.objects.all()
    context = {"userinfo":userinfo[0],"imgs":imgs}
    print("*____________________"* 3)
    if request.method == "POST":
        """输入"""
        input_tasktype = request.POST.get("type",None)
        input_title = request.POST.get("title",None)
        input_description = request.POST.get("description",None)
        input_tags = request.POST.get("tags",None)
        input_status = request.POST.get("status",None)
        """需要添加"""
        input_ctime = initTime() 
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
    userinfo = UserInfo.objects.filter(username=username)
    taskid = taskidMD5(username)
    request.session['taskidMD5'] = taskid
    taskinfo = tasks.objects.all().filter(id=input_task_id)
    imglist = IMG.objects.all().filter(task_id=input_task_id)
    context = {"userinfo":userinfo[0],"taskinfo":taskinfo[0],"imglist":imglist,"task_id":input_task_id}
    if input_task_id != None:
        if request.method == "POST":
            taskinfolist = tasks.objects.all()
            context = {"userinfo":userinfo[0],"taskinfolist":taskinfolist}
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
    userinfo = UserInfo.objects.filter(username=username)
    taskinfolist = tasks.objects.all()
    """获取复选框内容"""
    check_box_list = request.GET.getlist('ids[]')
    """获取id对象"""
    for input_task_id in check_box_list:
        """获取id的对象"""
        taskinfo = tasks.objects.filter(id=input_task_id)
        """删除任务图片"""
        img = IMG.objects.all().filter(task_id=input_task_id)
        if len(img) > 0:
            os.remove(MEDIA_ROOT+ "/img/" + img[0].name)
        """移除task"""
        taskinfo.delete()

        

    context = {"userinfo":userinfo[0],"taskinfolist":taskinfolist}
    return HttpResponseRedirect('/task/tasklist.html',context)
@login_require
def starttask(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    taskinfolist = tasks.objects.all()
    """获取复选框值"""
    check_box_list = request.GET.getlist('ids[]')
    """点击启动，如何启动时间为None则修改启动时间，修改task状态"""
    for input_task_id in check_box_list:
        """获取id的对象"""
        taskinfo = tasks.objects.filter(id=input_task_id)
        """只有状态是未启动【0】的时候才会启动"""
        if taskinfo[0].status == 0:
            taskinfo.update(status=1)
        """修改启动时间"""
        if taskinfo[0].s_time == None:
            input_stime = initTime() 
            taskinfo.update(s_time=input_stime)
    context = {"userinfo":userinfo[0],"taskinfolist":taskinfolist}
    return HttpResponseRedirect('/task/tasklist.html',context)
@login_require
def complatetask(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    taskinfolist = tasks.objects.all()
    context = {"userinfo":userinfo[0],"taskinfolist":taskinfolist}
    """获取复选框值"""
    check_box_list = request.GET.getlist('ids[]')
    """获取taskid对象"""
    for input_task_id in check_box_list:
        """获取对象"""
        taskinfo = tasks.objects.filter(id=input_task_id)
        """只有状态为进行中的时候才可以修改状态"""
        """修改完成时间"""
        if taskinfo[0].status == 1:
            input_ftime = initTime() 
            taskinfo.update(status=2,f_time=input_ftime)
    return HttpResponseRedirect('/task/tasklist.html',context)
@login_require
def add_task_point(request):
    input_task_id = request.GET.get("task_id",None)
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    context = {"userinfo":userinfo[0],"task_point_info":task_point_info,"task_id":input_task_id}
    if input_task_id != None:
        context = {"userinfo":userinfo[0],"task_point_info":task_point_info,"task_id":input_task_id}
        if request.method == "POST":
            input_ctime = initTime()
            input_status = request.POST.get("type",None)
            input_title = request.POST.get("title",None) 
            if input_title != None:
                if input_status != 2:
                    new_task_point = task_point(
                        title = input_title,
                        c_time = input_ctime,
                        f_time = input_ctime,
                        status = input_status,
                        task_id = input_task_id
                    )
                    new_task_point.save() 
                else:
                    new_task_point = task_point(
                        title = input_title,
                        c_time = input_ctime,
                        status = input_status,
                        task_id = input_task_id
                    )
                    new_task_point.save()
              
    else:
        context = {"userinfo":userinfo[0],"task_point_info":task_point_info,"status":"没有如此ID","task_id":None}
    return render(request,'task/add_task_point.html',context)

@login_require
def del_task_point(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    input_task_id = request.GET.get("task_id",None)
    input_task_point_id = request.GET.get("task_point_id",None)
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    context = {"userinfo[0]":userinfo[0],"task_point_info":task_point_info,"status":"没有如此ID"}
    task_point_info = task_point.objects.all().filter(id=input_task_point_id)    
    if len(task_point_info) == 1:
        task_point_info.delete()
    else:
        return HttpResponse("没有如此ID")
    return HttpResponseRedirect('/task/add_task_point/?task_id={}'.format(input_task_id))
"""点击完成小任务"""
@login_require
def done_task_point(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    input_task_id = request.GET.get("task_id",None)
    input_task_point_id = request.GET.get("task_point_id",None)
    taskinfo = tasks.objects.all().filter(id=input_task_id)
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    task_point1 = task_point.objects.all().filter(id=input_task_point_id)
    context = {"userinfo":userinfo[0],"task_point_info":task_point_info,"task_id":input_task_id,"task_point1":task_point1[0]}
    input_f_time = initTime() 
    if task_point1[0].status != 2:
        task_point1.update(status=2)
    if task_point1[0].f_time == None:
        task_point1.update(f_time=input_f_time)
    if  taskinfo[0].s_time == None: 
        taskinfo.update(s_time=input_f_time)
    if  taskinfo[0].status == 0:
        taskinfo.update(status= 1)
    return HttpResponseRedirect('/task/add_task_point/?task_id={}'.format(input_task_id),context)


@login_require
def edit_task_point(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    input_task_id = request.GET.get("task_id",None)
    input_task_point_id = request.GET.get("task_point_id",None)
    task_point_info = task_point.objects.all().filter(task_id=input_task_id)
    task_point1 = task_point.objects.all().filter(id=input_task_point_id)
    context = {"userinfo":userinfo[0],"task_point_info":task_point_info,"task_id":input_task_id,"task_point1":task_point1[0]}
    if request.method == "POST":
        input_f_time = initTime() 
        input_title = request.POST.get("title",None)
        input_status = request.POST.get("type",None)
        task_point1.update(title=input_title,status=input_status)
        if input_status == "2":
            task_point1.update(f_time=input_f_time)
        else:
            task_point1.update(f_time=None)
    return render(request,'task/edit_task_point.html',context)

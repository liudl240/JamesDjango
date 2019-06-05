from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response,HttpResponsePermanentRedirect
from upload.models import IMG
from JamesDjango.settings import MEDIA_URL 
import os,base64 
from Task.models import tasks
import json
# Create your views here.

def uploadImg(request):
    if request.method == 'POST':
        print(request.FILES.get('file',None))
        input_id = request.GET.get('id',None)
        if request.FILES.get('file',None) != None:
            new_img = IMG(
                img=request.FILES.get('file'),
                name = request.FILES.get('file').name,
                id = input_id,
            )
        new_img.save()
        print("这是图片名字:"+ request.POST.get("name",None))
        print("这是图片UID:"+ request.POST.get("uid",None))
        print("这是图片ID:"+ request.POST.get("id",None))
        print("这是图片类型:"+ request.POST.get("type",None))
        print("这是图片最后修改时间:"+ request.POST.get("lastModifiedDate",None))
        print("这是图片大小:"+ request.POST.get("size",None))

        print("*" * 30 )
        print(request.FILES['file'])
        #for imginfo in imgListInfo:
        #    print(imgInfo)
        print(request.POST)
        print(request.GET)
    return  HttpResponse("请先选择图片再上传")
"""
def uploadImg(request):
    if request.method == 'POST':
        print(request.FILES.get('img',None))
        if request.FILES.get('img',None) != None:
            new_img = IMG(
                img=request.FILES.get('img'),
                name = request.FILES.get('img').name
            )
            new_img.save()
            request.session["username"].append(new_img.id)
            username = request.session.get("username", None)
            imgs=IMG.objects.all()
            context = {"username":username,"imgs":imgs}
            return HttpResponseRedirect( '/task/addtask.html', context)
        else:
            return  HttpResponse("请先选择图片再上传")
    return render(request, 'upload/uploadimg.html')
"""
def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    for i in imgs:
        print (i.img.url)
    return render(request, 'upload/showimg.html', content)

def delImg(request):
    input_task_id = request.GET.get("task_id",None)
    if input_task_id != None:
        username = request.session.get("username", None)
        taskinfo = tasks.objects.all().filter(id=input_task_id)
        imglist = IMG.objects.all().filter(task_id=input_task_id)
        input_taskimg_id = request.GET.get("taskimg_id",None)
        img = IMG.objects.all().filter(id=input_taskimg_id)
        if input_taskimg_id != None:
           img.delete() 
        context = {"username":username,"taskinfo":taskinfo[0],"imglist":imglist,"task_id":input_task_id}
        return HttpResponseRedirect('/task/edittask.html?task_id={}'.format(input_task_id),context )
    else:
        return HttpResponse("没有如此ID")

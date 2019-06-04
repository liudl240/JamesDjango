from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response,HttpResponsePermanentRedirect
from upload.models import IMG
from JamesDjango.settings import MEDIA_URL 
import os,base64 
import json
# Create your views here.



def uploadImg(request):
    if request.method == 'POST':
        print(request.FILES.get('file',None))
        if request.FILES.get('file',None) != None:
            new_img = IMG(
                img=request.FILES.get('file'),
                name = request.FILES.get('file').name
            )
        new_img.save()
        print("这是图片名字:"+ request.POST.get("name",None))
        print("这是图片UID:"+ request.POST.get("uid",None))
        print("这是图片ID:"+ request.POST.get("id",None))
        print("这是图片类型:"+ request.POST.get("type",None))
        print("这是图片最后修改时间:"+ request.POST.get("lastModifiedDate",None))
        print("这是图片大小:"+ request.POST.get("size",None))
        #print("这是图片大小:"+ request.FILES)

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
    del_id = request.GET.get("id",None)
    id_info = IMG.objects.all().filter(id=del_id)
    if len(id_info) > 0:
        id_info.delete()
    else:
        return HttpResponse("没有这个ID")
    username = request.session.get("username", None)
    imgs=IMG.objects.all()
    context = {"username":username,"imgs":imgs}
    return HttpResponseRedirect( '/task/addtask.html', context)

from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response
from upload.models import IMG
import json
# Create your views here.

def uploadImg(request):
    if request.method == 'POST':
        # imgname=json.loads(request.body.decode())[0].get("name")
        # new_img = IMG(
        #     img=request.FILES.get('img'),
        #     name = request.FILES.get('img').name
        # )
        # new_img.save()
        imgListInfo = json.loads(request.body.decode())
        for imageinfo in imgListInfo:
            print(imageinfo.get("name"))
            new_img = IMG(
                img = imageinfo.get("base64"),
                name = imageinfo.get("name"),
            )
            new_img.save()
        return HttpResponseRedirect( '/users/userlist')
    return render(request, 'upload/uploadimg.html')

def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    for i in imgs:
        print (i.img.url)
    return render(request, 'upload/showimg.html', content)
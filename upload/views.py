from django.shortcuts import render
from upload.models import IMG
# Create your views here.

def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()
    return render(request, 'upload/uploadimg.html')

def showImg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs':imgs,
    }
    for i in imgs:
        print (i.img.url)
    return render(request, 'upload/showimg.html', content)
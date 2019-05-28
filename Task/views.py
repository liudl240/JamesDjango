from django.shortcuts import render

# Create your views here.

def tasklist(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/tasklist.html',context)

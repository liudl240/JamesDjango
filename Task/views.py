from django.shortcuts import render

# Create your views here.

def tasklist(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/tasklist.html',context)


def addtask(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/addtask.html',context)

def edittask(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/edittask.html',context)

def deltask(request):
    username = request.session.get("username", None)
    context = {"username":username}
    return render(request,'task/deltask.html',context)

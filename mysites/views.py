from django.shortcuts import render, render_to_response
from Users.views import login_require
"""主页"""
@login_require
def index(request):
    username = request.session.get("username", None)
    if username == None:
        return render(request,"Users/login.html")
    else:
        context = {"username":username}
        return render(request, 'index.html',context)


"""404页面"""
def page_not_found(request):
    return render_to_response('404.html')

"""500页面"""
def page_error(request):
    return render_to_response('500.html')
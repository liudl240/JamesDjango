from django.shortcuts import render
from Users.views import login_require
"""主页"""
@login_require
def index(request):
    return render(request, 'index.html')

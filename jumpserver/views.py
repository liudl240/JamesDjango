from django.shortcuts import render, HttpResponse,HttpResponseRedirect 
from jumpserver.tools.tools import unique
from Users.models import UserInfo
from JamesDjango.settings import TMP_DIR
from Users.views import login_require
import os


import requests
import json
from pprint import pprint

"""连接服务器"""
@login_require
def connection_host(request):
    username = request.session.get("username",None)
    userinfo = UserInfo.objects.filter(username=username)
    context = {"userinfo":userinfo[0]}
    return render(request, 'jumpserver/connection_host.html',context)

"""增加主机"""
@login_require
def add_host(request):
    return render(request,'jumpserver/add_host.html')

"""编辑"""

"""增加登录用户"""
@login_require
def add_login_user(request):
    return render(request,'jumpserver/add_login_user')

"""增加用户组"""
@login_require
def add_group(request):
    return render(request,'jumpserver/add_group')

"""增加密钥"""
@login_require
def upload_ssh_key(request):
    if request.method == 'POST':
        pkey = request.FILES.get('pkey')
        ssh_key = pkey.read().decode('utf-8')

        while True:
            filename = unique()
            ssh_key_path = os.path.join(TMP_DIR, filename)
            if not os.path.isfile(ssh_key_path):
                with open(ssh_key_path, 'w') as f:
                    f.write(ssh_key)
                break
            else:
                continue

        return HttpResponse(filename)

def jumpserver(request):
    url = 'http://192.168.0.194:8030/api/users/v1/auth/'
    query_args = {
        "username": "admin",
        "password": "admin"
    }
    response = requests.post(url, data=query_args)

    token=json.loads(response.text)['token']
    print(token)
    return HttpResponseRedirect ('http://192.168.0.194:8030?csrfmiddlewaretoken={_token}&username=admin&password=admin'.format(_token=token))

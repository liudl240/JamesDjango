from django.shortcuts import render, HttpResponse,redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from Users.captcha import create_validate_code
from django.contrib import messages
from io import BytesIO
from Users import models

"""用户登陆限制"""
def login_require(func):
    def wrapper(request, *args, **kwargs):
        username = request.session.get("username", None)
        if not username:
            return render(request, "Users/login.html")
        else:
            res = func(request, *args, **kwargs)
            return res
    return wrapper

def captcha(request):
    f = BytesIO()
    img,code = create_validate_code()
    request.session['code'] = code
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())

"""登陆页面"""
def login(request):
    error_msg="" 
    if request.method == 'POST':
        input_username = request.POST.get('username','none') 
        input_password = request.POST.get('password','none')
        input_captcha = request.POST.get("captcha", None)
        captcha = request.session.get("code", None)
        print(captcha,input_captcha)
        if captcha.lower() != input_captcha.lower(): 
            error_msg="验证码错误"
            return render(request, "Users/login.html", {'error_msg':error_msg})
        userinfo = models.UserInfo.objects.all().filter(username=input_username)
        if len(userinfo) > 0:
            if input_username == userinfo[0].username:
                if check_password(input_password,userinfo[0].password):
                    print("登陆成功")
                    request.session["username"] = input_username
                    context={'username':request.session.get("username")}
                    return render(request, 'index.html', context)
                else:
                    print("密码错误")
                    error_msg="密码错误"
                    return render(request, "Users/login.html", {'error_msg':error_msg})
            else:
                error_msg="用户不存在"
                return render(request, "Users/login.html", {'error_msg':error_msg})
        else:
            error_msg="请输入用户名"
            return render(request, "Users/login.html", {'error_msg':error_msg})
    return render(request, "Users/login.html", {'error_msg':error_msg})

"""用户列表|查看|编辑"""
def userlist(request):
    return render(request, 'Users/userlist.html')

"""增加用户"""
def adduser(request):
    return render(request, 'Users/adduser.html')

"""删除用户"""
def deluser(request):
    return render(request, 'Users/deluser.html')

"""修改用户"""
def edituser(request):
    return render(request, 'Users/edituser.html')

"""用户信息"""
@login_require
def userinfo(request):
    return render(request, 'Users/userinfo.html')

"""注销"""
def logout(request):
    username = request.session.get('username', None) 
    request.session.clear()
    return render(request, 'Users/login.html')

"""修改密码"""
def changepasswd(request):
    username = request.session.get("username", None) 
    context = {"username": username}
    if request.method == "POST":
        oldpassword = request.POST.get("oldpwd", None)
        newpassword = request.POST.get("newpwd", None)
        confirmpassword = request.POST.get("confirmpwd", None)
        userinfo = models.UserInfo.objects.all().filter(username=username)
        print(oldpassword,newpassword,confirmpassword)
        if check_password(oldpassword,userinfo[0].password) and newpassword == confirmpassword:
            newpwd=make_password(confirmpassword)
            userinfo.update(password=newpwd)
            return render(request, "index.html")
        else:
            return  HttpResponse("密码错误!!!")
    return render(request, "Users/changepasswd.html")
"""找回密码"""
def editpassword(request):
    return render(request,'Users/editpassword.html')

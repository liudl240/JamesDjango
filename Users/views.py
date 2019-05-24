from django.shortcuts import render, HttpResponse,redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, send_mass_mail
from Users.captcha import create_validate_code
from Users.emailcode import emailcode 
from django.contrib import messages
from JamesDjango import settings
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
"""获取图片验证码"""
def captcha(request):
    f = BytesIO()
    img,code = create_validate_code()
    request.session['code'] = code
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())


"""获取图片"""


"""获取邮箱验证码"""
def sendemail(request):
    email_code = emailcode()
    title = "JamesOps 自动化运维平台验证码"
    msg = "【JamesOps - 自动化运维平台】您的邮箱验证码为:{_code}，请确保本人操作，以免带来不必要损失，感谢您的使>用。".format(_code=email_code)
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        'liudl24@163.com'
    ]
    # 发送邮件
    status = "发送成功！！"
    send_mail(title, msg, email_from, reciever)
    return render(request, "Users/editpassword.html", {'error_msg':status})
    

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
    if request.method == "POST":
        input_email = request.POST.get("email",None)
        input_captcha = request.POST.get("captcha",None)
        input_Vcode = request.POST.get("Vcode",None)
        input_password = request.POST.get("password",None)
        input_confirm_password = request.POST.get("confirm_password",None)
        captcha = request.session.get("code", None)
        if captcha.lower() != input_captcha.lower():
            error_msg="验证码错误"
            return render(request, "Users/editpassword.html", {'error_msg':error_msg})
        #print(input_email+"输入验证码:"+input_Vcode +"输入密码:"+ input_password + "确认密码："+input_confirm_password +"输入验证码" + captcha+ "code :" + captcha) 
    return render(request,'Users/editpassword.html')

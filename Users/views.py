from django.shortcuts import render, HttpResponse,redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, send_mass_mail
from Users.captcha import create_validate_code
from Users.emailcode import emailcode 
from django.contrib import messages
from JamesDjango import settings
from io import BytesIO
from Users import models
from datetime import *
import time

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




"""获取邮箱验证码"""
def sendemail(request):
    status = ""
    print("GGGGGGGGGGGGG")
    if request.method == 'POST':
        input_email = request.POST.get("email",None)
        print("输入的邮箱是："+input_email)
        if input_email == "":
            error_msg = "该邮箱不能为空！"
            return render(request, "Users/sendemail.html", {'error_msg': error_msg})
        print(input_email)
        emailinfo = models.UserInfo.objects.filter(email=input_email)
        if len(emailinfo) == 0:
            error_msg = "该邮箱并没有注册！"
            return render(request, "Users/sendemail.html", {'error_msg': error_msg})
        else:
            request.session['input_email'] = input_email
            email_code = emailcode()
            request.session['emailcode'] = email_code
            title = "JamesOps 自动化运维平台验证码"
            msg = "【JamesOps - 自动化运维平台】您的邮箱验证码为:{_code}，请确保本人操作，以免带来不必要损失，感谢您的使用。".format(_code=email_code)
            email_from = settings.DEFAULT_FROM_EMAIL
            reciever = [
                input_email
            ]
            # #发送邮件
            send_mail(title, msg, email_from, reciever)
            print(email_code,request.session.get("email"))
            status = "发送成功，请登录邮箱查收！"
            print(status)
            return render(request, "Users/editpassword.html", {'error_msg': status})
        return render(request, "Users/login.html", {'error_msg': status})
    return render(request, "Users/sendemail.html", {'error_msg': status})


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
                if userinfo[0].active == 0:
                    print("禁止登录")
                    error_msg="禁止登录"
                    return render(request, "Users/login.html", {'error_msg':error_msg})
                elif check_password(input_password,userinfo[0].password):
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
@login_require
def userlist(request):
    username = request.session.get("username",None)
    userlist = models.UserInfo.objects.all()
    context = {"userlist":userlist,"username":username}
    return render(request, 'Users/userlist.html',context)



"""增加用户"""
def adduser(request):
    if request.method == "POST":
        input_username = request.POST.get("username",None)
        input_password = request.POST.get("password", None)
        input_confirm_password = request.POST.get("confirm_password", None)
        input_captcha = request.POST.get("captcha", None)
        input_email = request.POST.get("email", None)
        captcha = request.session.get("code", None)
        input_argv=[input_username,input_password,input_confirm_password,input_captcha,input_email]
        userinfo = models.UserInfo.objects.filter(username=input_username)
        emailinfo = models.UserInfo.objects.filter(email=input_email)
        for argv in input_argv :
            if argv == None:
                error_msg = "必须全部填写"
                return render(request, "Users/adduser.html", {'error_msg': error_msg})
            else:
                if len(userinfo) > 0:
                    error_msg = "用户已存在"
                    return render(request, "Users/adduser.html", {'error_msg': error_msg})
                if len(emailinfo) > 0:
                    error_msg = "该邮箱已经注册了用户！"
                    return render(request, "Users/adduser.html", {'error_msg': error_msg})
                if input_password != input_confirm_password:
                    error_msg = "两次输入的密码不一致"
                    return render(request, "Users/adduser.html", {'error_msg': error_msg})
                elif captcha.lower() != input_captcha.lower():
                    error_msg = "验证码错误"
                    return render(request, "Users/adduser.html", {'error_msg': error_msg})
                password = make_password(input_password)
                email = input_email
                c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(c_time)
                models.UserInfo.objects.create(username=input_username, password=password,email=email,c_time=c_time)
                status = "恭喜，注册成功"
                return render(request, 'Users/login.html', {'error_msg':status})
    return render(request, 'Users/adduser.html')


"""删除用户"""
@login_require
def deluser(request):
    edit_id = request.GET.get("id", None)
    idinfo = models.UserInfo.objects.filter(id=edit_id)
    userinfo = models.UserInfo.objects.all()
    username = request.session.get("username", None)
    if len(idinfo) == 0 :
        context = {"error_msg": "没有这个id用户","userinfo":userinfo,"username":username}
        return HttpResponseRedirect( '/users/userlist', context)
    idinfo.delete()
    print("删除成功")
    status="删除成功"
    context = {"error_msg": status,"userinfo":userinfo,"username":username}
    return HttpResponseRedirect( '/users/userlist', context)

"""修改用户"""
@login_require
def edituser(request):
    edit_id = request.GET.get("id", None)
    idinfo = models.UserInfo.objects.filter(id=edit_id)
    username = request.session.get("username", None)
    print(username,idinfo[0].username)
    context = {"username":username,"idinfo":idinfo[0]}
    if request.method == "POST":
        input_username = request.POST.get("username",None)
        input_email = request.POST.get("email",None)
        input_active = request.POST.get("active",None)
        input_password = request.POST.get("password",None)    
        edit_id = request.GET.get("id", None)
        username = request.session.get("username", None)
        idinfo = models.UserInfo.objects.filter(id=edit_id)
        context = {"username":username, "idinfo":idinfo[0]}
        if input_username == "" and input_email == "" and input_active == "" and input_password == "":
            status="输入为空，没有修改！"
            context = {"error_msg": status,"userinfo":userinfo,"username":username}
            return HttpResponseRedirect( '/users/userlist', context)
        elif input_username != "" or input_email !="":
            userinfo = models.UserInfo.objects.filter(username=input_username) 
            emailinfo = models.UserInfo.objects.filter(email=input_email) 
            if len(userinfo) > 0 or len(emailinfo) > 0:
                status="用户名或者邮箱已存在，不能修改！"
                context = {"error_msg": status,"userinfo":userinfo,"username":username}
                return HttpResponseRedirect( '/users/userlist', context)
        if input_username != "":
            idinfo.update(username=input_username) 
        elif input_email != "":
            idinfo.update(email=input_email) 
        elif input_active != "":
            idinfo.update(active=input_active)
        elif input_password != "":
            idinfo.update(password=make_password(input_password))
        status="修改成功，请查阅"
        userinfo = models.UserInfo.objects.all()
        context = {"error_msg": status,"userinfo":userinfo,"username":username}
        return HttpResponseRedirect( '/users/userlist', context)
    return render(request, 'Users/edituser.html',context)

"""用户信息"""
@login_require
def userinfo(request):
    username = request.session.get("username", None)
    userinfo = models.UserInfo.objects.filter(username=username)
    context = {"username": username,"userinfo":userinfo[0]}
    if request.method == "POST":
        input_nickname = request.POST.get("nickname",None)
        input_email = request.POST.get("email",None)
        input_remark = request.POST.get("remark",None)
        userinfo.update(nickname=input_nickname,email=input_email,remark=input_remark)
        return HttpResponseRedirect( '/users/userinfo', context)
    return render(request, 'Users/userinfo.html',context)

"""注销"""
@login_require
def logout(request):
    username = request.session.get('username', None) 
    request.session.clear()
    userinfo = models.UserInfo.objects.filter(username=username)
    l_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    userinfo.update(l_time=l_time)
    return render(request, 'Users/login.html')

"""修改密码"""
@login_require
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
            return render(request, "index.html",context)
        else:
            status = "旧密码错误"
            return render(request, 'Users/login.html', {'error_msg': status})
    return render(request, "Users/changepasswd.html")
"""忘记密码"""
@login_require
def editpassword(request):
    if request.method == "POST":
        input_captcha = request.POST.get("captcha",None)
        input_emailcode = request.POST.get("emailcode",None)
        input_password = request.POST.get("password",None)
        input_confirm_password = request.POST.get("confirm_password",None)
        input_email = request.session.get("input_email")
        captcha = request.session.get("code", None)
        emailcode = request.session.get("emailcode", None)
        emailinfo = models.UserInfo.objects.all().filter(email=input_email)

        if  emailcode != input_emailcode:
            error_msg = "邮箱验证码错误"
            return render(request, "Users/editpassword.html", {'error_msg': error_msg})
        elif captcha.lower() != input_captcha.lower():
            error_msg="验证码错误"
            return render(request, "Users/editpassword.html", {'error_msg':error_msg})
        #print(input_email+"输入验证码:"+input_Vcode +"输入密码:"+ input_password + "确认密码："+input_confirm_password +"输入验证码" + captcha+ "code :" + captcha) 
        elif input_password != input_confirm_password:
            error_msg = "两次输入的密码不一致"
            return render(request, "Users/adduser.html", {'error_msg': error_msg})
        elif len(emailinfo) ==0:
            error_msg = "该邮箱没有注册的用户"
            return render(request, "Users/adduser.html", {'error_msg': error_msg})
        emailinfo.update(password =make_password(input_password))
        status = "恭喜，修改密码成功"
        return render(request, 'Users/login.html', {'error_msg': status})
    return render(request,'Users/editpassword.html')

@login_require
def reviewuser(request):
    username = request.session.get("username", None)
    userlist = models.UserInfo.objects.all().order_by('-active')
    context = {"username": username,"userlist":userlist}
    edit_id = request.GET.get("id",None)
    edit_active = request.GET.get("active",None)
    if edit_id == "" or edit_active == "":
        status="修改失败，请联系管理员"
        context = {"username": username,"userlist":userlist,"error_msg":status}
    else:
        models.UserInfo.objects.filter(id=edit_id).update(active=edit_active)
        status="审核成功" 
        context = {"username": username,"userlist":userlist,"error_msg":status}
    return render(request,"Users/reviewuser.html",context)

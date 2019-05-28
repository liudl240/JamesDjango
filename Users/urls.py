from django.urls import path
from django.conf.urls import include, url
from Users import views

urlpatterns = [
    url('login', views.login, name='login'),
    url('sendemail', views.sendemail, name='sendemail'),
    url('captcha', views.captcha, name='captcha'),
    url('logout', views.logout, name='logout'),
    url('userlist', views.userlist, name='userlist'),
    url('adduser', views.adduser, name='adduser'),
    url('userinfo', views.userinfo, name='userinfo'),
    url('deluser', views.deluser, name='deluser'),
    url('edituser', views.edituser, name='edituser'),
    url('changepasswd', views.changepasswd, name='changepasswd'),
    url('editpassword', views.editpassword, name='editpassword'),
]

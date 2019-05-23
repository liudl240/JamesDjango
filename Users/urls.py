from django.urls import path
from django.conf.urls import include, url
from Users import views

urlpatterns = [
    url('login', views.login, name='login'),
    url('captcha', views.captcha, name='captcha'),
    url('logout', views.logout, name='logout'),
    url('userlist', views.userlist, name='userlist'),
    url('adduser', views.adduser, name='adduser'),
    url('userinfo', views.userinfo, name='userinfo'),
    url('changepasswd', views.changepasswd, name='changepasswd'),
    url('editpassword', views.editpassword, name='editpassword'),
]

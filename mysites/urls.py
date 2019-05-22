from django.urls import path
from django.conf.urls import include, url
from mysites import views

urlpatterns = [
    url('', views.index, name='index'),
]

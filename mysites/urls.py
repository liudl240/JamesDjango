from django.urls import path
from django.conf.urls import include, url
from mysites import views
from django.conf.urls import handler404, handler500

urlpatterns = [
    url('servicelist', views.servicelist, name='servicelist'),
    url('editservice', views.editservice, name='editservice'),
    url('delservice', views.delservice, name='delservice'),
    url('', views.index, name='index'),
]
#handler404 = "mysites.views.page_not_found"

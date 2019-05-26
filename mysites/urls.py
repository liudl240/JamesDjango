from django.urls import path
from django.conf.urls import include, url
from mysites import views
from django.conf.urls import handler404, handler500

urlpatterns = [
    url('', views.index, name='index'),
]
#handler404 = "mysites.views.page_not_found"
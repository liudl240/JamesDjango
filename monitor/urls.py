from django.urls import path
from django.conf.urls import include, url
from monitor import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('company/listinfo', views.listinfo, name='listinfo'),
    url('company/addinfo', views.addinfo, name='addinfo'),
    url('company/delinfo', views.delinfo, name='delinfo'),
    url('company/editinfo', views.editinfo, name='editinfo'),
]

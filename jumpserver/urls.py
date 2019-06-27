from django.urls import path
from django.conf.urls import include, url
from jumpserver import views

urlpatterns = [
    url('connection_host', views.connection_host, name='connection_host'),
    url('upload_ssh_key', views.upload_ssh_key, name='upload_ssh_key'),
]

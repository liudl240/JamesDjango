from django.urls import path
from django.conf.urls import include, url
from Task import views

urlpatterns = [
    url('tasklist', views.tasklist, name='tasklist'),
    url('addtask', views.addtask, name='addtask'),
    url('edittask', views.edittask, name='edittask'),
    url('deltask', views.deltask, name='deltask'),
]

from django.urls import path
from django.conf.urls import include, url
from Task import views

urlpatterns = [
    url('tasklist', views.tasklist, name='tasklist'),
    url('addtask', views.addtask, name='addtask'),
    url('edittask', views.edittask, name='edittask'),
    url('deltask', views.deltask, name='deltask'),
    url('starttask', views.starttask, name='starttask'),
    url('complatetask', views.complatetask, name='complatetask'),
    url('add_task_point', views.add_task_point, name='add_task_point'),
    url('del_task_point', views.del_task_point, name='del_task_point'),
    url('edit_task_point', views.edit_task_point, name='edit_task_point'),
]

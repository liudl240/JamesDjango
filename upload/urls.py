from django.urls import path
from django.conf.urls import include, url
from upload import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('uploadimg', views.uploadImg, name='uploadImg'),
    url('showimg', views.showImg, name='showImg'),
]
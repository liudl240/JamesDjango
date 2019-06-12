from django.urls import path
from wiki import views
from django.conf.urls import include, url

urlpatterns = [
    url('wikilist', views.wikilist, name='wikilist'),
    url('adddoc', views.adddoc, name='adddoc'),
    url('editdoc', views.editdoc, name='editdoc'),
    url('deldoc', views.deldoc, name='deldoc'),
]

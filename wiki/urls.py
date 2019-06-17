from django.urls import path
from wiki import views
from django.conf.urls import include, url

urlpatterns = [
    url('wikilist', views.wikilist, name='wikilist'),
    url('Solve_doc', views.Solve_doc, name='Solve_doc'),
    url('savedoc', views.savedoc, name='savedoc'),
    url('editdoc', views.editdoc, name='editdoc'),
    url('deldoc', views.deldoc, name='deldoc'),
]

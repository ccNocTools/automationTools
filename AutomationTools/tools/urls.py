from django.conf.urls import url
from . import views

app_name = 'tools'

urlpatterns = [
    url(r'^get_os/$', views.get_os, name='get_os'),
    url(r'^find_os/$', views.find_os, name='find_os'),
    url(r'^locate_host/$', views.locate_host, name='locate_host'),
    url(r'^locate_host_ajax/$', views.locate_host_ajax, name='locate_host_ajax')
]

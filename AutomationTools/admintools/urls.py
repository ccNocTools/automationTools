from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

app_name = 'admintools'

urlpatterns = [
    url(r'^users$', views.users, name='users'),
    url(r'^new_user/$', views.new_user, name='new_user'),
    url(r'^modify_user$', views.modify_user, name='modify_user'),
    url(r'^community_string$', views.community_string, name='community_string'),
    url(r'^device_database$', views.device_database, name='device_database'),
    url(r'^reset_all$', views.reset_all, name='reset_all')
]

from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

app_name = 'admintools'

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^adduser/$', views.add_user, name='add_user'),
    url(r'^newuser/$', views.new_user, name='new_user'),
    url(r'^modifyuser$', views.modify_user, name='modify_user')
]

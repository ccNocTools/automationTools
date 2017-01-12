from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name='index'), #/
    url(r'^initialize/$', views.initialize, name='initialize'), #/initialize/
    url(r'^login/$', views.login_attempt, name='login'),
    url(r'^home/$', views.index, name='home'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register')
]

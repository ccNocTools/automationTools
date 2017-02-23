from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.home, name='home'), #/
    url(r'^initialize/$', views.initialize, name='initialize'),
    url(r'^login/$', views.login_attempt, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_options/$', views.user_options, name='user_options')
]

from django.conf.urls import patterns, include, url
from mainapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('mainapp.views',
    url(r'^login/$', 'login', name = 'login'),
    url(r'^agenda/$', 'agenda', name = 'agenda'),
    url(r'^profile/$', 'profile', name = 'profile'),
    url(r'^enterEvent/$', 'enterEvent', name = 'enterEvent'),
    url(r'^userProfile/$', 'userProfile', name = 'userProfile'),
    url(r'^getMatchedEvents/$', 'getMatchedEvents', name = 'getMatchedEvents'),
)
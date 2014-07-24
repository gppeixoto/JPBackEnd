from django.conf.urls import patterns, include, url
from mainapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('mainapp.views',
    url(r'^login/$', 'login', name = 'login'),
    url(r'^useragenda/$', 'userAgenda', name = 'userAgenda'),
    url(r'^userprofile/$', 'userProfile', name = 'userProfile'),
    url(r'^enterevent/$', 'enterEvent', name = 'enterEvent'),
    url(r'^create/$', 'createEvent', name = 'createEvent'),
    url(r'^getmatchedevents/$', 'getMatchedEvents', name = 'getMatchedEvents'),
    url(r'^testgetmatchedevents/$', 'testgetmatchedevents', name='testgetmatchedevents'),
    url(r'^testlogin/$', 'testlogin', name='testlogin'),
    url(r'^testcreate/$', 'testcreate', name='testcreate'),
)
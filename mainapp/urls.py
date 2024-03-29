from django.conf.urls import patterns, include, url
from mainapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('mainapp.views',
    url(r'^login/$', 'login', name = 'login'),
    url(r'^useragenda/$', 'userAgenda', name = 'userAgenda'),
    url(r'^userprofile/$', 'userProfile', name = 'userProfile'),
    url(r'^userprofileid/$', 'userProfileId', name = 'userProfileId'),
    url(r'^enterevent/$', 'enterEvent', name = 'enterEvent'),
    url(r'^leaveevent/$', 'leaveEvent', name = 'leaveEvent'),
    url(r'^createevent/$', 'createEvent', name = 'createEvent'),
    url(r'^deleteevent/$', 'deleteEvent', name = 'deleteEvent'),
    url(r'^editevent/$', 'editEvent', name = 'editEvent'),
    url(r'^getmatchedevents/$', 'getMatchedEvents', name = 'getMatchedEvents'),
    url(r'^getevent/$', 'getEvent', name = 'getEvent'),
    url(r'^getdistance/$', 'getDistance', name = 'getDistance'),
    url(r'^voteintaguser/$', 'voteInTagUser', name = 'voteInTagUser'),
    url(r'^rateuser/$', 'rateUser', name = 'rateUser'),
    url(r'^comment/$', 'comment', name = 'comment'),
    url(r'^invite/$', 'invite', name = 'invite'),
    url(r'^getfriends/$', 'getFriends', name = 'getFriends'),
    url(r'^getinvites/$', 'getInvites', name = 'getInvites'),
    url(r'^getaddresses/$', 'getAddresses', name = 'getAddresses'),
    url(r'^getversion/$', 'getVersion', name = 'getVersion'),
    url(r'^getfutureevents/$', 'getFutureEvents', name = 'getFutureEvents'),
    url(r'^closeevent/$', 'closeEvent', name = 'closeEvent'),
    url(r'^arrive/$', 'arrive', name = 'arrive'),
    url(r'^cancelarrive/$', 'cancelArrive', name = 'cancelArrive'),
    url(r'^getpast/$', 'getPast', name = 'getPast'),
    url(r'^testgetmatchedevents/$', 'testGetMatchedEvents', name='testGetMatchedEvents'),
    url(r'^testlogin/$', 'testLogin', name='testLogin'),
    url(r'^testcreateevent/$', 'testCreateEvent', name='testCreateEvent'),
    url(r'^testeditevent/$', 'testEditEvent', name = 'testEditEvent'),
    url(r'^testenterevent/$', 'testEnterEvent', name = 'testEnterEvent'),
    url(r'^testleaveevent/$', 'testLeaveEvent', name = 'testLeaveEvent'),
    url(r'^testuserprofile/$', 'testUserProfile', name = 'testUserProfile'),
    url(r'^testuserprofileid/$', 'testUserProfileId', name = 'testUserProfileId'),
    url(r'^testvoteintaguser/$', 'testVoteInTagUser', name = 'testVoteInTagUser'),
    url(r'^testrateuser/$', 'testRateUser', name = 'testRateUser'),
    url(r'^testheroku/$', 'testHeroku', name = 'testHeroku'),
    url(r'^testgetevent/$', 'testGetEvent', name = 'testGetEvent'),
    url(r'^testcomment/$', 'testComment', name = 'testComment'),
    url(r'^testinvite/$', 'testInvite', name = 'testInvite'),
    url(r'^testgetfriends/$', 'testgetFriends', name = 'testgetFriends'),
    url(r'^testgetinvites/$', 'testGetInvites', name = 'testGetInvites'),
    url(r'^testuseragenda/$', 'testUserAgenda', name = 'testUserAgenda'),
    url(r'^testgetfutureevents/$', 'testGetFutureEvents', name = 'testGetFutureEvents'),
    url(r'^testcloseevent/$', 'testCloseEvent', name = 'testCloseEvent'),
    url(r'^testarrive/$', 'testArrive', name = 'testArrive'),
    url(r'^testcancelarrive/$', 'testCancelArrive', name = 'testCancelArrive'),
    url(r'^testgetpast/$', 'testGetPast', name = 'testGetPast'),
    
)

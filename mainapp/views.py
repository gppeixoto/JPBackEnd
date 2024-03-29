#encoding:utf-8

from django.shortcuts import render
import requests
from models import Sport, Rating
from django.contrib.auth.models import User
from django_facebook.connect import connect_user
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
from django_facebook.api import *
from open_facebook.api import *
from mainapp.models import *
import time
from decimal import Decimal
from django.shortcuts import render, redirect
import urllib2
import urllib
from util import *
from DatabaseJP.settings import APP_CURRENT_VERSION

# Create your views here.

url_base = "http://join-play.herokuapp.com/"
# url_base = "http://localhost:8000/"

def connect(request, access_token):
    action, user = connect_user(request, access_token)
    profile = Profile.objects.get(user=user)
    return profile, FacebookUserConverter(OpenFacebook(access_token))

def login(request):
    data = json.loads(request.read())
    print data
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    return HttpResponse(json.dumps(profile.getUserProfile(fb_user)), content_type="application/json")

def cmp(event):
    date = event.date
    time = event.timeBegin
    date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond, tzinfo=time.tzinfo)
    return date

def userAgenda(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    events = Event.objects.filter(persons=profile, date__gte=str(datetime.datetime.today().date()))
    events = sorted(list(events), key=cmp)
    eventList = [event.getEvent(fb_user) for event in events]

    if 'localization' in data:
        localization = data['localization']
        toSortArray = []
        i = 0
        for event in eventList:
            completeLocalization = event['localizationAddress'] + '+' + event['neighbourhood'] + '+' + event['city']
            toSortArray.append((getDistance(localization, completeLocalization), i))
            i += 1
        retSortedEvents = []
        for nextId in toSortArray:
            actDict = eventList[nextId[1]]
            actDict['localizationDistance'] = nextId[0]
            retSortedEvents.append(actDict)
    else:
        retSortedEvents = eventList

    return HttpResponse(json.dumps({'events' : retSortedEvents}), content_type="application/json")

def getPast(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    events = Event.objects.filter(persons=profile, date__lte=str(datetime.datetime.today().date()))
    events = reversed(sorted(list(events), key=cmp))
    eventList = [event.getEvent(fb_user) for event in events]

    if 'localization' in data:
        localization = data['localization']
        toSortArray = []
        i = 0
        for event in eventList:
            completeLocalization = event['localizationAddress'] + '+' + event['neighbourhood'] + '+' + event['city']
            toSortArray.append((getDistance(localization, completeLocalization), i))
            i += 1
        retSortedEvents = []
        for nextId in toSortArray:
            actDict = eventList[nextId[1]]
            actDict['localizationDistance'] = nextId[0]
            retSortedEvents.append(actDict)
    else:
        retSortedEvents = eventList

    return HttpResponse(json.dumps({'events' : retSortedEvents}), content_type="application/json")


def userProfile(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    userInfo = profile.getUserProfile(fb_user)
    return HttpResponse(json.dumps(userInfo), content_type="application/json")

def userProfileId(request):
    data = json.loads(request.read())
    uId = data['uId']
    id = data['id']
    profile = Profile.objects.get(facebook_id=id)
    userProfile = Profile.objects.get(facebook_id=uId)
    # we need to find a way to handle expiring token issues
    # saving friends in bd seems a valid idea
    access_token = profile.access_token
    fb_user = FacebookUserConverter(OpenFacebook(access_token))
    userInfo = profile.getUserProfile(fb_user)
    userInfo = appendInfo(userInfo, profile, userProfile)
    return HttpResponse(json.dumps(userInfo), content_type="application/json")

def getFutureEvents(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    events = Event.objects.filter(date__gte=str(datetime.datetime.today().date()), opened=True)

    profile, fb_user = connect(request, access_token)
    publicEvents = events.filter(private=False)
    visibleEvents = events.filter(private=True, visible=profile)
    retEvents = [event.getEvent(fb_user) for event in (publicEvents | visibleEvents).distinct()]

    if 'localization' in data:
        localization = data['localization']
        toSortArray = []
        i = 0
        for event in retEvents:
            completeLocalization = event['localizationAddress'] + '+' + event['neighbourhood'] + '+' + event['city']
            toSortArray.append((getDistance(localization, completeLocalization), i))
            i += 1
        toSortArray.sort()
        retSortedEvents = []
        for nextId in toSortArray:
            actDict = retEvents[nextId[1]]
            actDict['localizationDistance'] = nextId[0]
            retSortedEvents.append(actDict)
    else:
        retSortedEvents = retEvents

    return HttpResponse(json.dumps({'events' : retSortedEvents}), content_type="application/json")

def getMatchedEvents(request):
    data = json.loads(request.read())
    events = Event.objects.filter(opened=True)
    qDate = data['date']
    if qDate != "":
        events = events.filter(date__gte=qDate)
    qTimeBegin = data['start_time']
    if qTimeBegin != "":
        events = events.filter(timeBegin__gte=qTimeBegin)
    qTimeEnd = data['end_time']
    if qTimeEnd != "":
        events = events.filter(timeEnd__lte=qTimeEnd)
    qSport = data['sports']
    if qSport != []:
        sports = [Sport.objects.get(name__iexact=sport) for sport in qSport if len(Sport.objects.filter(name__iexact=sport)) != 0]
        print sports
        events = events.filter(sport__in=sports)
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    publicEvents = events.filter(private=False)
    visibleEvents = events.filter(private=True, visible=profile)
    print publicEvents
    retEvents = [event.getEvent(fb_user) for event in (publicEvents | visibleEvents).distinct()]

    qAddress = data['address']
    if qAddress != "":
        toSortArray = []
        i = 0
        for event in retEvents:
            completeLocalization = event['localizationAddress'] + '+' + event['neighbourhood'] + '+' + event['city']
            toSortArray.append((getDistance(qAddress, completeLocalization), i))
            i += 1
        toSortArray.sort()
        retSortedEvents = []
        for nextId in toSortArray:
            actDict = retEvents[nextId[1]]
            actDict['localizationDistance'] = nextId[0]
            retSortedEvents.append(actDict)
    else:
        retSortedEvents = retEvents

    '''
    try:
        prevSearch = Search.objects.get(person=profile)
        prevSearch.delete()
    except Search.DoesNotExist:
        pass

    # update when localization is fixed
    newSearch = Search(person=profile, date=qDate, timeBegin=qTimeBegin, timeEnd=qTimeEnd)
    newSearch.save()
    for sport in qSport:
        newSearch.sport.add(Sport.objects.get(name=sport))
    newSearch.save()
    '''

    return HttpResponse(json.dumps({"events" : retSortedEvents}), content_type="application/json")

def getEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    evt_id = data['id']
    event = Event.objects.get(id=evt_id)
    profile, fb_user = connect(request, access_token)
    retEvent = event.getDetailedEvent(fb_user)
    return HttpResponse(json.dumps({"event" : retEvent}), content_type="application/json")

def enterEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.persons.add(profile)
    event.save()
    return HttpResponse(json.dumps(event.getEvent(fb_user)), content_type="application/json")

def leaveEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.persons.remove(profile)
    event.save()
    return HttpResponse(json.dumps(event.getDetailedEvent(fb_user)), content_type="application/json")


def arrive(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.arrived.add(profile)
    event.save()
    return HttpResponse(json.dumps(event.getDetailedEvent(fb_user)), content_type="application/json")

def cancelArrive(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.arrived.remove(profile)
    event.save()
    return HttpResponse(json.dumps(event.getDetailedEvent(fb_user)), content_type="application/json")

def createEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    localizationName = data['localizationName']
    localizationAddress = data['localizationAddress']
    city = data['city']
    neighbourhood = data['neighbourhood']
    eventLocalization, _ = Localization.objects.get_or_create(name=localizationName, adress=localizationAddress,neighbourhood=neighbourhood,city=city)
    sportName = data['eventSport']
    eventSport = Sport.objects.get(name=sportName)
    eventDay = data['eventDay']
    eventTimeBegin = data['eventTimeBegin']
    eventTimeEnd = data['eventTimeEnd']
    eventDescription = data['eventDescription']
    eventName = data['eventName']
    eventPrice = Decimal(data['eventPrice'])
    private = data['private']
    newEvent = Event(name=eventName, creatorProfile=profile, description=eventDescription, localization=eventLocalization,
                    sport=eventSport, date=eventDay, timeBegin=eventTimeBegin, timeEnd=eventTimeEnd,
                    price=eventPrice,private=private)
    if 'latitude' in data:
        newEvent.lat = data['latitude']
    if 'longitude' in data:
        newEvent.lng = data['longitude']
    newEvent.save()
    id = newEvent.id;
    newEvent.persons.add(profile)
    if private:
        newEvent.visible.add(profile)
    # we need to query the event because of formatting issues
    bdEvent = Event.objects.get(id=id)
    return HttpResponse(json.dumps(bdEvent.getDetailedEvent(fb_user)), content_type="application/json")

def editEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    localizationName = data['localizationName']
    localizationAddress = data['localizationAddress']
    city = data['city']
    neighbourhood = data['neighbourhood']
    eventLocalization, _ = Localization.objects.get_or_create(name=localizationName, adress=localizationAddress,neighbourhood=neighbourhood,city=city)
    sportName = data['eventSport']
    eventSport = Sport.objects.get(name=sportName)
    eventDay = data['eventDay']
    eventTimeBegin = data['eventTimeBegin']
    eventTimeEnd = data['eventTimeEnd']
    eventDescription = data['eventDescription']
    eventName = data['eventName']
    eventPrice = Decimal(data['eventPrice'])
    private = data['private']
    id = data['id']
    event = Event.objects.get(id=id)
    if event.creatorProfile.facebook_id != profile.facebook_id:
        return HttpResponse(json.dumps({"error":"error"}), content_type="application/json")
    newEvent = Event(id=id,name=eventName, creatorProfile=profile, description=eventDescription, localization=eventLocalization,
                    sport=eventSport, date=eventDay, timeBegin=eventTimeBegin, timeEnd=eventTimeEnd,
                    price=eventPrice,private=private)
    if 'latitude' in data:
        newEvent.lat = data['latitude']
    if 'longitude' in data:
        newEvent.lng = data['longitude']
    newEvent.save()
    # we need to query the event because of formatting issues
    bdEvent = Event.objects.get(id=id)
    return HttpResponse(json.dumps(bdEvent.getDetailedEvent(fb_user)), content_type="application/json")

def deleteEvent(request):
    data = json.loads(request.read())
    userId = data['user_id']
    evtId = data['event_id']
    event = Event.objects.get(id=evtId)
    if event.creatorProfile.facebook_id != userId:
        return HttpResponse(json.dumps({"error":"error"}), content_type="application/json")
    event.delete()
    return HttpResponse(json.dumps({"Nothing":"Nothing"}), content_type="application/json")


def voteInTagUser(request):
    data = json.loads(request.read())
    voterId = data['v_id']
    userId = data['id']
    tagName = data['tag']
    profile = Profile.objects.get(facebook_id=userId)
    tag, _ = Tag.objects.get_or_create(name=tagName, person=profile)
    tag.performTag()
    tag.save()
    voterProfile = Profile.objects.get(facebook_id=voterId)
    vote = Vote(voter=voterProfile, voted=profile, tag=tag)
    vote.save()
    # the code will loke better if we somehow call userProfileId from here
    access_token = profile.access_token
    fb_user = FacebookUserConverter(OpenFacebook(access_token))
    userInfo = profile.getUserProfile(fb_user)
    userInfo = appendInfo(userInfo, profile, voterProfile)
    return HttpResponse(json.dumps(userInfo), content_type="application/json")

def rateUser(request):
    data = json.loads(request.read())
    voterId = data['v_id']
    userId = data['id']
    sportName = data['sport']
    value = data['value']
    profile = Profile.objects.get(facebook_id=userId)
    sport = Sport.objects.get(name=sportName)
    rating, _ = Rating.objects.get_or_create(sport=sport, person=profile)
    rating.rate(value)
    rating.save()
    voterProfile = Profile.objects.get(facebook_id=voterId)
    vote = Vote(voter=voterProfile, voted=profile, sport=sport)
    vote.save()
    # the code will loke better if we somehow call userProfileId from here
    access_token = profile.access_token
    fb_user = FacebookUserConverter(OpenFacebook(access_token))
    userInfo = profile.getUserProfile(fb_user)
    userInfo = appendInfo(userInfo, profile, voterProfile)
    return HttpResponse(json.dumps(userInfo), content_type="application/json")

def comment(request):
    data = json.loads(request.read())
    evtId = data['event_id']
    userId = data['user_id']
    comentario = data['comment']
    profile = Profile.objects.get(facebook_id=userId)
    evento = Event.objects.get(id=evtId)
    new_comment = Comment(event=evento,person=profile,text=comentario,time=datetime.datetime.now().time(),day=datetime.datetime.today().date())
    new_comment.save()
    foto = getUserImageUrl(profile.facebook_id)
    nome = profile.facebook_name
    date = datetime.datetime.now() - datetime.timedelta(hours=3)
    day = str(date).split(" ")[0]
    time = str(date).split(" ")[1]
    time = time[:time.find(".")]
    return HttpResponse(json.dumps({"photo":foto,"name":nome,"day":day, "time":time}), content_type="application/json")

def invite(request):
    data = json.loads(request.read())
    listUsers = data['user_id_list']
    evtId = data['event_id']
    userId = data['id']
    event = Event.objects.get(id=evtId)
    # project decision
    # if event.creatorProfile.facebook_id != userId:
    #   return HttpResponse(json.dumps({"error":"error"}), content_type="application/json")
    for user_id in listUsers:
        profile = Profile.objects.get(facebook_id=user_id)
        event.visible.add(profile)
    event.save()
    return HttpResponse(json.dumps({'user_id_list' : listUsers}), content_type="application/json")

def getFriends(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    listFriendsId = [friend['id'] for friend in fb_user.get_friends()]
    listFriends = []
    for friendId in listFriendsId:
        try:
           nextFriend = Profile.objects.get(facebook_id=friendId)
        except Profile.DoesNotExist:
           nextFriend = None
        if nextFriend is not None:
            dic = appendInfo({}, nextFriend, profile)
            tags = dic['tagVotes']
            listFriends.append((friendId, nextFriend.facebook_name, getUserImageUrl(friendId), tags))
    return HttpResponse(json.dumps({'friends':listFriends}), content_type="application/json")

def getInvites(request):
    data = json.loads(request.read())
    uId = data['id']
    profile = Profile.objects.get(facebook_id=uId)
    try:
        invites = Event.objects.filter(visible=profile, opened=True)
        inviteList = {}
        for invite in invites:
            formattedDate = invite.date.strftime("%d/%m")
            if invite.date < datetime.datetime.today().date():
                continue
            if profile in invite.persons.all():
                continue
            formattedTimeBegin = invite.timeBegin.strftime("%H:%M")
            formattedInvite = {'creator' : invite.creatorProfile.facebook_name, 'creatorImage' : getUserImageUrl(invite.creatorProfile.facebook_id), 'eventName' : invite.name, 'timeBegin' : formattedTimeBegin, 'date' : formattedDate, 'private' : invite.private, 'id' : invite.id, 'localizationName' : invite.localization.name, 'neighbourhood' : invite.localization.neighbourhood}
            prevList = inviteList.get(invite.sport.name, [])
            prevList.append(formattedInvite)
            inviteList[invite.sport.name] = prevList
        if inviteList != {}:
            return HttpResponse(json.dumps({'inviteList':inviteList}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'no invites for you':'no invites for you'}), content_type="application/json")
    except Event.DoesNotExist:
        return HttpResponse(json.dumps({'no invites for you':'no invites for you'}), content_type="application/json")

def closeEvent(request):
    data = json.loads(request.read())
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.opened = False
    event.save()
    return HttpResponse(json.dumps({"closed" : "closed"}), content_type="application/json")

def getVersion(request):
    return HttpResponse(json.dumps({"version" : APP_CURRENT_VERSION}))

#going to front-end
'''
def getAddresses(request):
    data = json.loads(request.read())
    textLocalName = data['local_name']
    textStreet = data['street']
    textNeighbourhood = data['neighbourhood']
    textCity = data['city']
    queryText = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    queryText += textLocalName+" "
    queryText += textStreet+" "
    queryText += textNeighbourhood+" "
    queryText += textCity
    queryText += "&sensor=true&key=AIzaSyDL-BaFaZBo_evgT2pXRJ1avAb8sWZ3KGE"
    page = requests.get(queryText).text
    result = json.loads(page)
    # print result
    formattedAddresses = []
    for address in result['results']:
        formattedAddresses.append(address['formatted_address'])
    return HttpResponse(json.dumps({'formatted_addresses':formattedAddresses}))
'''

# sends a http post to the url that we want to test,
# simulating future uses
def viewTester(data, url):
    try:
        req = urllib2.Request(url_base + url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        return HttpResponse(response.read(), content_type="application/json")
    except HTTPError as e:
        return HttpResponse(e.read())

def testGetMatchedEvents(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'address' : "menlo park",
        'date' : "",
        'start_time' : "",
        'end_time' : "",
        'sports' : []
    }

    return viewTester(data, 'getmatchedevents/')

def testLogin(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Mateus Moury').access_token,
    }

    return viewTester(data, 'login/')

def testCreateEvent(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'localizationName' : 'UFPE',
        'localizationAddress' : 'Av. Jorn. Aníbal Fernandes',
        'city' : 'Recife',
        'neighbourhood' : 'Cidade Universitaria',
        'eventSport' : 'Futebol',
        'eventDay' : '2014-12-12',
        'eventTimeBegin' : '14:30',
        'eventTimeEnd' : '19:00',
        'eventDescription' : 'Bla bla bla',
        'eventName' : 'A',
        'eventPrice' : '60.00',
        'private' : True,
        'latitude': '-8.039573000000001',
        'longitude': '-34.899502'
    }

    return viewTester(data, 'createevent/')

def testEditEvent(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'localizationName' : 'CIn - UFPE',
        'localizationAddress' : 'Av. Jornalista Anibal Fernandes',
        'city' : 'Recife',
        'neighbourhood' : 'Cidade Universitaria',
        'eventSport' : 'Futebol',
        'eventDay' : '2014-08-20',
        'eventTimeBegin' : '08:00',
        'eventTimeEnd' : '12:00',
        'eventDescription' : 'Demo day',
        'eventName' : 'Campeonato de Ping pong do Join&Play',
        'eventPrice' : '0.00',
        'private' : False,
        'latitude': '-8.04973000000001',
        'longitude': '-34.899502',
        'id' : '39'
    }

    return viewTester(data, 'editevent/')

def testEnterEvent(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Mateus Moury').access_token,
        'id' : 39
    }

    return viewTester(data, 'enterevent/')

def testLeaveEvent(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Mateus Moury').access_token,
        'id' : 39,
    }

    return viewTester(data, 'leaveevent/')

def testUserProfile(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Mateus Moury').access_token,
    }

    return viewTester(data, 'userprofile/')

def testUserProfileId(request):
    data = {
        'id' : Profile.objects.get(facebook_name="Mateus Moury").facebook_id,
        'uId' : Profile.objects.get(facebook_name="Lucas Lima").facebook_id
    }

    return viewTester(data, 'userprofileid/')

def testVoteInTagUser(request):
    data = {
        'tag' : 'Fair Play',
        'id' : Profile.objects.get(facebook_name='Mateus Moury').facebook_id,
        'v_id' : Profile.objects.get(facebook_name='Lucas Lima').facebook_id
    }

    return viewTester(data, 'voteintaguser/')

def testRateUser(request):
    data = {
        'sport' : 'Futebol',
        'value' : 2,
        'id' : '687719994632948',
        'v_id':'628143283960150'
    }

    return viewTester(data, 'rateuser/')

def testHeroku(request):
    access_token = Profile.objects.get(facebook_name='Mateus Moury').access_token
    profile = Profile.objects.get(access_token=access_token)
    fb_user = FacebookUserConverter(OpenFacebook(access_token))
    return HttpResponse(json.dumps(profile.getUserProfile(fb_user)), content_type="application/json")

def testGetEvent(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'id' : 39
    }
    return viewTester(data, 'getevent/')

def testComment(request):
    data = {
        'event_id' : '39',
        'user_id' : Profile.objects.get(facebook_name='Lucas Lima').facebook_id,
        'comment' : 'Teste do horario'
    }
    return viewTester(data, 'comment/')

def testInvite(request):
    data = {
        'event_id' : 39,
        'id' : Profile.objects.get(facebook_name='Lucas Lima').facebook_id,
        'user_id_list' : [Profile.objects.get(facebook_name='Mateus Moury').facebook_id]
    }
    return viewTester(data, 'invite/')

def testgetFriends(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Mateus Moury').access_token
    }
    return viewTester(data, 'getfriends/')

def testGetInvites(request):
    data = {
        'id' : Profile.objects.get(facebook_name='Mateus Moury').facebook_id
    }
    return viewTester(data, 'getinvites/')

def testUserAgenda(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'localization' : '-8.039573000000001,-34.899502'
    }
    return viewTester(data, 'useragenda/')

def testGetPast(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'localization' : '-8.039573000000001,-34.899502'
    }
    return viewTester(data, 'getpast/')

def testGetFutureEvents(request):
    data = {
        'access_token' : 'CAAJ6iZBGS5FIBAGfiSDxZAEWF15B1NbGbjyyHR81aWmZA7qYeihi6nE1zo67xqDgX5p4NmfpjZCPPoZADQHjd1oICZAvEilu4pPitKeOyQ6HQIFZCzerMzFre8JCyg9yghZAlCpZBZC6nv1cUNb0JJUEHCUqzTdKqthq6ac0zpNGk7M8V2vqkYgcWZB7sSlAkvHWqzCrDyTO56LvZCZCDH7flWaEQTUKRLjVQEVZBqZA9e4AicSCgZDZD'#Profile.objects.get(facebook_name='Lucas Lima').access_token,
        #'localization' : '-.05576671,-34.95200721'
    }
    return viewTester(data, 'getfutureevents/')

def testCloseEvent(request):
    data = {
        'id' : 39
    }
    return viewTester(data, 'closeevent/')

def testArrive(request):
    data = {
        'access_token' : Profile.objects.get(facebook_name='Lucas Lima').access_token,
        'id' : 39
    }

    return viewTester(data, 'arrive/')

def testCancelArrive(request):
    data = {
        'access_token' : 'CAAJ6iZBGS5FIBAGAjtXAxbpONpW1xJBo1PcoeKQkwVWPLJC8okuf4D4eYt8aS1l21f6erZBZAQg9BNqPZAiuls4bsZBAZCxwwTHCaQsIsV0899xsD4qievDsgvHmlGhysC9WcFifuI9EwLpgUHtnT71p4WItZAl35uhNwIFYjnYxFOMyfgb7OJvSpNmJSSydFcZD',
        'id' : 39,
    }

    return viewTester(data, 'cancelarrive/')

#going to front-end
'''
def testGetAddresses(request):
    data = {
        'local_name' : 'Centro de Informatica UFPE',
        'street' : '',
        'neighbourhood' : '',
        'city' : ''
    }
    return viewTester(data, 'getaddresses/')
'''

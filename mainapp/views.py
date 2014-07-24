from django.shortcuts import render
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

# Create your views here.

def connect(request, access_token):
    action, user = connect_user(request, access_token)
    profile = Profile.objects.get(user=user)
    return profile, FacebookUserConverter(OpenFacebook(access_token))

def login(request):
    data = json.loads(request.read())
    print request.read()
    print data
    access_token = data['access_token']
    print access_token 
    profile, fb_user = connect(request, access_token)
    return HttpResponse(json.dumps(profile.getUserProfile(fb_user)['information']), content_type="application/json")

def userAgenda(request):
    data = json.loads(request.read())
    access_token = data['access_token'] 
    profile, fb_user = connect(request, access_token)
    eventList = [event.getEvent(fb_user) for event in Event.objects.filter(persons=profile)]
    return HttpResponse(json.dumps(eventList), content_type="application/json")

def userProfile(request):
    data = json.loads(request.read())
    access_token = data['access_token'] 
    profile, fb_user = connect(request, access_token)
    userInfo = profile.getUserProfile(fb_user)
    return HttpResponse(json.dumps(userInfo), content_type="application/json")

def getMatchedEvents(request):
    data = json.loads(request.read())
    events = Event.objects.all()
    qAddress = data['address']
    if qAddress != "":
        localization = Localization.objects.get(address=qAddress)
        events = Event.filter(localization=localization)
    qDate = data['date']
    if qDate != "":
        events = events.filter(date=qDate)
    qTimeBegin = data['start_time']
    if qTimeBegin != "":
        events = events.filter(timeBegin__gte=qTimeBegin)
    qTimeEnd = data['end_time']
    if qTimeEnd != "":
        events = events.filter(timeEnd__lte=qTimeEnd)
    qSport = data['sports']
    if qSport != []:
        sports = [Sport.objects.get(name=sport) for sport in qSport]
        events = events.filter(sport__in=sports)
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    retEvents = [event.getEvent(fb_user) for event in events]
    return HttpResponse(json.dumps({"events" : retEvents}), content_type="application/json")

def enterEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.persons.add(profile)
    event.save()
    return HttpResponse(json.dumps(event.getEvent(fb_user)), content_type="application/json")

# def createEvent(request):
#     data = json.loads(request.read())
#     access_token = data['access_token']
#     profile, fb_user = connect(request, access_token)
#     localizationName = data['localizationName']
#     localizationAddress = data['localizationAddress']
#     eventLocalization = Localization.objects.get_or_create(name=localizationName, adress=localizationAddress)
#     sportName = data['eventSport']
#     eventSport = Sport.objects.get(name=sportName)
#     eventDay = time.strptime(data['eventDay'], "%d %m %Y")
#     eventTime = time.strptime(date['eventTime'], "%H %M")
#     eventDescription = data['eventDescription']
#     eventName = data['eventName']
#     eventPrice = Decimal(data['eventPrice'])
#     newEvent = Event(name=eventName, description=eventDescription, localization=eventLocalization, 
#                     sport=eventSport, date=eventDay, time=eventTime, price=eventPrice)
#     newEvent.persons.add(profile)
#     newEvent.save()
#     return HttpResponse(json.dumps(newEvent.getEvent(fb_user)), content_type="application/json")


def testegetmatchedevents(request):
    data = {
        'access_token' : 'CAAJ6iZBGS5FIBAPnlmlZBMC5K450EzoaZC44mBmlhWPwZBRkzi6BVBZC96gP5YE8qa9ArODtxPqVLkEj8eqiHdXcyrvvG9rZCnKjtOanZCf5ewq3CiHy6am1PYZC8f1CP7gOVT1o6jBwOZA2ff1JyZBMXZBY7wDnvH2w1orhuP575UZAoCSRvzX9s6LfAKg6LMsyZCiIZD', 'address' : "", 'date' : "2014-07-19", 'start_time' : "", 'end_time' : "", 'sports' : []
    }

    try:
        req = urllib2.Request('http://192.168.0.110:8000/getmatchedevents/')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        return HttpResponse(response.read())
    except HTTPError as e:
        return HttpResponse(e.read())

def testelogin(request):
    data = {
        'access_token' : 'CAAJ6iZBGS5FIBAPnlmlZBMC5K450EzoaZC44mBmlhWPwZBRkzi6BVBZC96gP5YE8qa9ArODtxPqVLkEj8eqiHdXcyrvvG9rZCnKjtOanZCf5ewq3CiHy6am1PYZC8f1CP7gOVT1o6jBwOZA2ff1JyZBMXZBY7wDnvH2w1orhuP575UZAoCSRvzX9s6LfAKg6LMsyZCiIZD'
    }

    try:
        req = urllib2.Request('http://192.168.0.110:8000/login/')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        return HttpResponse(response.read())
    except HTTPError as e:
        return HttpResponse(e.read())
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
    print data
    access_token = data['access_token']
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
    newEvent = Event(name=eventName, description=eventDescription, localization=eventLocalization, 
                    sport=eventSport, date=eventDay, timeBegin=eventTimeBegin, timeEnd=eventTimeEnd,
                    price=eventPrice,private=private)
    newEvent.save()
    id = newEvent.id;
    newEvent.persons.add(profile)
    bdEvent = Event.objects.get(id=id)
    return HttpResponse(json.dumps(bdEvent.getEvent(fb_user)), content_type="application/json")


def testgetmatchedevents(request):
    data = {
        'access_token' : 'CAAJ6iZBGS5FIBAPnlmlZBMC5K450EzoaZC44mBmlhWPwZBRkzi6BVBZC96gP5YE8qa9ArODtxPqVLkEj8eqiHdXcyrvvG9rZCnKjtOanZCf5ewq3CiHy6am1PYZC8f1CP7gOVT1o6jBwOZA2ff1JyZBMXZBY7wDnvH2w1orhuP575UZAoCSRvzX9s6LfAKg6LMsyZCiIZD',
        'address' : "",
        'date' : "",
        'start_time' : "",
        'end_time' : "",
        'sports' : []
    }

    try:
        req = urllib2.Request('http://192.168.0.110:8000/getmatchedevents/')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        return HttpResponse(response.read())
    except HTTPError as e:
        return HttpResponse(e.read())

def testlogin(request):
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

def testcreate(request):
    data = {
        'access_token' : 'CAAJ6iZBGS5FIBAPnlmlZBMC5K450EzoaZC44mBmlhWPwZBRkzi6BVBZC96gP5YE8qa9ArODtxPqVLkEj8eqiHdXcyrvvG9rZCnKjtOanZCf5ewq3CiHy6am1PYZC8f1CP7gOVT1o6jBwOZA2ff1JyZBMXZBY7wDnvH2w1orhuP575UZAoCSRvzX9s6LfAKg6LMsyZCiIZD',
        'localizationName' : 'CIn - UFPE',
        'localizationAddress' : 'Av. Jornalista Anibal Fernandes',
        'city' : 'Recife',
        'neighbourhood' : 'Cidade Universitaria',
        'eventSport' : 'Ping Pong',
        'eventDay' : '2014-08-18',
        'eventTimeBegin' : '08:00',
        'eventTimeEnd' : '12:00',
        'eventDescription' : 'Demo day',
        'eventName' : 'Ping pong do Demo Day',
        'eventPrice' : '0.00',
        'private' : False,
    }

    try:
        req = urllib2.Request('http://192.168.0.110:8000/create/')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        return HttpResponse(response.read())
    except HTTPError as e:
        return HttpResponse(e.read())
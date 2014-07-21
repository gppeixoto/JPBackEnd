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

# Create your views here.

def connect(request, access_token):
    action, user = connect_user(request, access_token)
    profile = Profile.objects.get(user=user)
    return profile, FacebookUserConverter(OpenFacebook(access_token))

def getMatchedEvents(request):
    data = json.loads(request.read())
    # data = {'access_token' : 'CAAJ6iZBGS5FIBAPnlmlZBMC5K450EzoaZC44mBmlhWPwZBRkzi6BVBZC96gP5YE8qa9ArODtxPqVLkEj8eqiHdXcyrvvG9rZCnKjtOanZCf5ewq3CiHy6am1PYZC8f1CP7gOVT1o6jBwOZA2ff1JyZBMXZBY7wDnvH2w1orhuP575UZAoCSRvzX9s6LfAKg6LMsyZCiIZD', 'address' : "", 'date' : "", 'time' : "", 'sports' : ["Futebol"]}
    events = Event.objects.all()
    qAddress = data['address']
    if qAddress != "":
        localization = Localization.objects.get(address=qAddress)
        events = Event.filter(localization=localization)
    qDate = data['date']
    if qDate != "":
        events = events.filter(date=qDate)
    qTime = data['time']
    if qTime != "":
        events = events.filter(time__lte=qTime)
    qSport = data['sports']
    if qSport != []:
        sports = [Sport.objects.get(name=sport) for sport in qSport]
        events = events.filter(sport__in=sports)
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    retEvents = [event.getEvent(fb_user) for event in events]
    return HttpResponse(json.dumps(retEvents), content_type="application/json")

def login(request):
    data = json.loads(request.read())
    access_token = data['access_token'] 
    # access_token = 'CAAJ6iZBGS5FIBAD1X9Hs6puxHso1itZAMERkA0Ez02biPTHbD1bClTDHaiKnYwFZAcdRbr0ITgAQoJNtGSmY0r89aFj6Y0MfmzCqZAkRAS1AAU1nRezZAPK14NlF4jbCdYC9qNPIvOkWIPhTJzyHAZBhzXkedpnG2eWcoNu2MaAfFYmulov3FrZBDYJGwlgkKrSGWMGvDw4XlTlNFW86rI9SbxbtvbEjT4ZD'
    profile, fb_user = connect(request, access_token)
    # redireciona pra alguma coisa 
    return HttpResponse(json.dumps(profile.getUserProfile(fb_user)['information']), content_type="application/json")

def agenda(request):
    data = json.loads(request.read())
    access_token = data['access_token'] 
    # access_token = 'CAAJ6iZBGS5FIBAKQXc6fPRoomdEFFvDr2SxF5NXCdm6tihH37INqywoelZCEXZCE44nCrNQpJI6eZB0BJSoiESkyGyqMbfmDNuFioNTFavmRX3KkjsIBhuXacJR73G9dr98cJWhw1mlG5417mRXZButu8pHd705FVBh52aZC3ZBmLNkIaHUlIMZAZATXjnWnJuhwZD'
    profile, fb_user = connect(request, access_token)
    eventList = [event.getEvent(fb_user) for event in Event.objects.filter(persons=profile)]
    return HttpResponse(json.dumps(eventList), content_type="application/json")

def userProfile(request):
    data = json.loads(request.read())
    access_token = data['access_token'] 
    # access_token = 'CAAJ6iZBGS5FIBAKQXc6fPRoomdEFFvDr2SxF5NXCdm6tihH37INqywoelZCEXZCE44nCrNQpJI6eZB0BJSoiESkyGyqMbfmDNuFioNTFavmRX3KkjsIBhuXacJR73G9dr98cJWhw1mlG5417mRXZButu8pHd705FVBh52aZC3ZBmLNkIaHUlIMZAZATXjnWnJuhwZD'
    profile, fb_user = connect(request, access_token)
    userInfo = profile.getUserProfile(fb_user)
    return HttpResponse(json.dumps(userInfo), content_type="application/json")

def enterEvent(request):
    data = json.loads(request.read())
    access_token = data['access_token']
    profile, fb_user = connect(request, access_token)
    eventId = data['id']
    event = Event.objects.get(id=eventId)
    event.persons.add(profile)
    event.save()
    return HttpResponse(json.dumps(event.getEvent(fb_user)), content_type="application/json")

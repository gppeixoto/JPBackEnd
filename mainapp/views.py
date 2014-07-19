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

def getMatchedEvents(qAdress, qDate, qTime, qSport, fb_user):
    sports = [Sport.objects.get(name=sport) for sport in qSport]
    localization = Localization.objects.get(adress=qAdress)
    events = Event.objects.filter(sport__in=sports, localization=localization, date=qDate, time__lte=qTime)
    retEvents = [event.getEvent(fb_user) for event in events]
    return retEvents

def login(request):
    # access_token = request.POST['access_token'] 
    access_token = 'CAAJ6iZBGS5FIBAD1X9Hs6puxHso1itZAMERkA0Ez02biPTHbD1bClTDHaiKnYwFZAcdRbr0ITgAQoJNtGSmY0r89aFj6Y0MfmzCqZAkRAS1AAU1nRezZAPK14NlF4jbCdYC9qNPIvOkWIPhTJzyHAZBhzXkedpnG2eWcoNu2MaAfFYmulov3FrZBDYJGwlgkKrSGWMGvDw4XlTlNFW86rI9SbxbtvbEjT4ZD'
    profile, fb_user = connect(request, access_token)
    # redireciona pra alguma coisa 
    return HttpResponse(json.dumps(profile.getUserProfile(fb_user)['information']), content_type="application/json")

def events(request):
    access_token = 'CAAJ6iZBGS5FIBAD1X9Hs6puxHso1itZAMERkA0Ez02biPTHbD1bClTDHaiKnYwFZAcdRbr0ITgAQoJNtGSmY0r89aFj6Y0MfmzCqZAkRAS1AAU1nRezZAPK14NlF4jbCdYC9qNPIvOkWIPhTJzyHAZBhzXkedpnG2eWcoNu2MaAfFYmulov3FrZBDYJGwlgkKrSGWMGvDw4XlTlNFW86rI9SbxbtvbEjT4ZD'
    profile, fb_user = connect(request, access_token)
    eventList = [event.getEvent(fb_user) for event in Event.objects.filter(persons=profile)]
    return HttpResponse(json.dumps(eventList), content_type="application/json")
from django.shortcuts import render
from django.contrib.auth.models import User
from django_facebook.connect import connect_user
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
from django_facebook.api import *
from open_facebook.api import *
import mainapp.models
import time
from decimal import Decimal
from django.shortcuts import render, redirect
import urllib2
import urllib
import requests

def isSimilar(search1, search2):
    if search1.person == search2.person:
        return False, None
    if search1.date != search2.date:
        return False, None
    if max(search1.timeBegin, search2.timeBegin) > min(search1.timeEnd, search2.timeEnd):
        return False, None
    commonSports = []
    otherSports = search2.sport.all()
    for sport in search1.sport.all():
        if sport in otherSports:
            commonSports.append(sport)
    if commonSports == []:
        return False, None

    intersection = {
        'person' : search2.person,
        'time_begin' : max(search1.timeBegin, search2.timeBegin),
        'time_end' : min(search2.timeEnd, search2.timeEnd),
        'sports' : commonSports
    }

    return True, intersection

def getSimilarSearches(mySearch):
    ret = []
    searches = mainapp.models.Search.objects.all()
    for search in searches:
        isIntersect, intersection = isSimilar(mySearch, search)
        if isIntersect:
            ret.append(intersection)
    return ret

def getDistance(origin, destiny):
    try:
        queryText = "http://maps.googleapis.com/maps/api/distancematrix/json?origins="
        queryText += origin
        queryText += "&destinations="
        queryText += destiny
        queryText += "&language=pt"
        page = requests.get(queryText).text
        result = json.loads(page)
        result = result['rows'][0]['elements'][0]['distance']
        return result['value']
    except Exception:
        return 10**9 + 7
def diff(time, day):
    now = datetime.datetime.now()
    comment = datetime.datetime(year=day.year, month=day.month, day=day.day, hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond, tzinfo=time.tzinfo)
    timeDiff = now - comment
    return timeDiff.days, timeDiff.seconds / 60

def diffTime(time, day):
    days, minutes = diff(time, day)
    return str(minutes / 60) + ":" + str(minutes % 60)

def diffDay(time, day):
    days, minutes = diff(time, day)
    return days   

def appendInfo(userInfo, profile, user):
    votes = mainapp.models.Vote.objects.filter(voter=user, voted=profile)
    tagVotes = []
    sportVotes = []
    for vote in votes:
        if vote.sport != None:
            sportVotes.append(vote.sport.name)
        elif vote.tag != None:
            tagVotes.append(vote.tag.name)
    userInfo['tagVotes'] = list(set(tagVotes))
    userInfo['sportVotes'] = list(set(sportVotes))
    return userInfo

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
    searches = Search.objects.all()
    for search in searches:
        isIntersect, intersection = isSimilar(mySearch, search)
        if isIntersect:
            ret.append(intersection)
    return ret

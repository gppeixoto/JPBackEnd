from django.shortcuts import render
from models import Sport, Rating
from django.contrib.auth.models import User
from django_facebook.connect import connect_user
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict

# Create your views here.

def login(request):
    # access_token = request.POST['access_token']
    access_token = 'CAAJ6iZBGS5FIBAPgnpVpmJNUPHWuhaLZC8jmu14hzZAbbZAPwDzTuFZA2LXhUS7OT4EcUbXbBduuH6hQKW6yCK1K71zRmc75ZBxmFIzTN3udNbo27UiH0yZBAESbTr9OyxZBOfEGNqnafy5pZAueZBEHy0ieDfQx8AtWDR9i3fCR5xH4lTksuKz44r5uO7YaKJs1EZD'
    action, user = connect_user(request, access_token)
    return HttpResponse(json.dumps(model_to_dict(user, fields=['username'], exclude=['date_of_birth'])), content_type="application/json")

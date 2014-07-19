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

def getFbUser(access_token):
    return FacebookUserConverter(OpenFacebook(access_token))

def login(request):
    # access_token = request.POST['access_token'] 
    access_token = 'CAAJ6iZBGS5FIBAD1X9Hs6puxHso1itZAMERkA0Ez02biPTHbD1bClTDHaiKnYwFZAcdRbr0ITgAQoJNtGSmY0r89aFj6Y0MfmzCqZAkRAS1AAU1nRezZAPK14NlF4jbCdYC9qNPIvOkWIPhTJzyHAZBhzXkedpnG2eWcoNu2MaAfFYmulov3FrZBDYJGwlgkKrSGWMGvDw4XlTlNFW86rI9SbxbtvbEjT4ZD'
    action, user = connect_user(request, access_token)
    profile = Profile.objects.get(user=user)
    fb_user = getFbUser(access_token)
    # redireciona pra alguma coisa 
    return HttpResponse(json.dumps(profile.getUserProfile(fb_user)['information']), content_type="application/json")

def image(request):
    filename = "C:\Users\Mateus\Documents\DatabaseJP\images\facebook_profiles\2014\07\fb_image_687719994632948.jpg" 
    response = HttpResponse(mimetype='application/force-download') 
    response['Content-Disposition']='attachment;filename="%s"'%filename
    response['Content-length'] = os.stat("debug.py").st_size
    return response
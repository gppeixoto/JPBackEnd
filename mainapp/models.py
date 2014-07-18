from django.db import models
from django.contrib.auth.models import User
from django_facebook.models import FacebookModel 
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django_facebook.utils import get_user_model, get_profile_model

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('users', filename)

class Profile(FacebookModel):
    user = models.OneToOneField(User)

@receiver(post_save) 
def create_profile(sender, instance, created, **kwargs):
    if sender == get_user_model():
        user = instance
        profile_model = get_profile_model() 
        if profile_model == Profile and created:
            profile, new = Profile.objects.get_or_create(user=instance)


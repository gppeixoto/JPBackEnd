from django.db import models
from django.contrib.auth.models import User
from django_facebook.models import FacebookModel 
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django_facebook.utils import get_user_model, get_profile_model
import os, datetime

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('sports', filename)

class Profile(FacebookModel):
    user = models.OneToOneField(User)

    def rate(self, sport, value):
        rating, _ = Rating.objects.get_or_create(person=self, sport=sport)
        rating.rate(value)
        rating.save()
        return rating

    def getTotalRating(self):
        ratings = Rating.objects.filter(person=self)
        numberOfVotes = 0
        ans = 0.0
        for rate in ratings:
            numberOfVotes += rate.numberOfVoters
            ans += rate.rating*rate.numberOfVoters
        if numberOfVotes == 0:
            return "Player not evaluated"
        else:
            return ans / numberOfVotes

    def inProfile(self, facebook_id):
        return len(Profile.objects.filter(facebook_id=facebook_id)) != 0


    def getUserProfile(self, fb_user):
        personalInformation = [self.facebook_name, self.getTotalRating()]
        sportRatings = Rating.objects.filter(person=self)
        ratingsInformation = [(sportRating.sport.name, sportRating.rating) for sportRating in sportRatings]
        friends = fb_user.get_friends()
        dbFriends = [(friend['id'], friend['name']) for friend in filter(lambda (dict): self.inProfile(dict['id']), friends)]
        photos = [Profile.objects.get(facebook_id=id).image for (id, _) in dbFriends]
        retFriends = [(id, name, image) for ((id,name), image) in zip(dbFriends, photos)]
        return [personalInformation, retFriends, ratingsInformation]


@receiver(post_save) 
def create_profile(sender, instance, created, **kwargs):
    if sender == get_user_model():
        user = instance
        profile_model = get_profile_model() 
        if profile_model == Profile and created:
            profile, new = Profile.objects.get_or_create(user=instance)

class Sport(models.Model):
    name = models.CharField(max_length=30)
    ratings = models.ManyToManyField(Profile, through='Rating')
    icon = models.ImageField(upload_to=get_image_path, blank=True, null=True) 

class Rating(models.Model):
    person = models.ForeignKey(Profile)
    sport = models.ForeignKey(Sport)
    numberOfVoters = models.IntegerField(default=0)
    rating = models.FloatField(default=2.5)

    def rate(self, value):
        if self.numberOfVoters == 0:
            self.rating = value
        else:
            self.rating = (self.rating * self.numberOfVoters + value) / (self.numberOfVoters + 1)
        self.numberOfVoters += 1


class Localization(models.Model):
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=200)

class Event(models.Model):
    persons = models.ManyToManyField(Profile)
    localization = models.ForeignKey(Localization)
    sport = models.ForeignKey(Sport)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(null=True)

    def getEvent(self):
        participants = [(friend.facebook_id, friend.facebook_name) for friend in self.persons.all()]
        photos = [Profile.objects.get(facebook_id=id).image for (id, _) in participants]
        retParticipants = [(id, name, image) for ((id,name), image) in zip(participants, photos)]
        return [retParticipants, [self.localization.name, self.localization.adress], self.sport.name, str(self.date), str(self.time)]


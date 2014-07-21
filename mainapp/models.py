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

def getUserImageUrl(image):
    return str(image)[str(image).find('/')+1:]

class Profile(FacebookModel):
    user = models.OneToOneField(User)
    notifications = models.BooleanField(default=True)

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
        personalInformation = [self.facebook_name, self.getTotalRating(), getUserImageUrl(self.image)]
        sportRatings = Rating.objects.filter(person=self)
        ratingsInformation = [(sportRating.sport.name, sportRating.rating) for sportRating in sportRatings]
        friends = fb_user.get_friends()
        dbFriends = [(friend['id'], friend['name']) for friend in filter(lambda (dict): self.inProfile(dict['id']), friends)]
        photos = [getUserImageUrl(Profile.objects.get(facebook_id=id).image) for (id, _) in dbFriends]
        retFriends = [(id, name, image) for ((id,name), image) in zip(dbFriends, photos)]
        retEvents = [event.getEvent(fb_user) for event in Event.objects.filter(persons=self)]
        return {"information" : personalInformation, "rating" : ratingsInformation, "events" : retEvents, "friends" : retFriends}


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
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    persons = models.ManyToManyField(Profile)
    localization = models.ForeignKey(Localization)
    sport = models.ForeignKey(Sport)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(null=True)
    description = models.CharField(max_length=2000)

    def getEvent(self, fb_user):
        participants = [(friend.facebook_id, friend.facebook_name) for friend in self.persons.all()]
        photos = [Profile.objects.get(facebook_id=id).image for (id, _) in participants]
        retParticipants = [(id, name, getUserImageUrl(image)) for ((id,name), image) in zip(participants, photos)]
        fbFriendsIds = [friend['id'] for friend in fb_user.get_friends()]
        commonFriends = len(filter(lambda (id, name, image): str(id) in fbFriendsIds, retParticipants))
        comments = [(comment.text, comment.person.facebook_name, comment.person.facebook_id) for comment in Comment.objects.filter(event=self)]
        return {"name" : self.name, "participants" : retParticipants, "localizationName" : self.localization.name,
                "localizationAddress" : self.localization.adress, "sport" : self.sport.name, "friends" : commonFriends,
                "date" : str(self.date), "time" : str(self.time), "description" : self.description, "comments" : comments,
                "id": self.id}

class Comment(models.Model):
    event = models.ForeignKey(Event)
    person = models.ForeignKey(Profile)
    text = models.CharField(max_length=2000)
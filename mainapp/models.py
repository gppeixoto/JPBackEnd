from django.db import models
from django.contrib.auth.models import User
from django_facebook.models import FacebookModel
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django_facebook.utils import get_user_model, get_profile_model
import os, datetime
from decimal import Decimal

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('sports', filename)

def getUserImageUrl(fb_id):
    return "https://graph.facebook.com/" + str(fb_id) + "/picture"

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
        sportRatings = Rating.objects.filter(person=self)
        ratingsInformation = [(sportRating.sport.name, sportRating.rating) for sportRating in sportRatings]
        sportsInformation = [(sport.name, Event.objects.filter(persons=self, sport=sport).count()) for sport in Sport.objects.all()]
        tags = Tag.objects.filter(person=self)
        tagsInformation = [(tag.name, tag.numberOfVoters) for tag in tags]
        friends = fb_user.get_friends()
        dbFriends = [(friend['id'], friend['name']) for friend in filter(lambda (dict): self.inProfile(dict['id']), friends)]
        return {"id": self.facebook_id, "name" : self.facebook_name, "url" : getUserImageUrl(self.facebook_id),
                "ratings" : ratingsInformation, "tags" : tagsInformation,
                "sportsInfo" : sportsInformation, "friends" : len(dbFriends),
                "notifications" : self.notifications}


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

class Tag(models.Model):
    person = models.ForeignKey(Profile)
    name = models.CharField(max_length=30)
    numberOfVoters = models.IntegerField(default=0)
    icon = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def tag(self):
        self.numberOfVoters += 1

class Localization(models.Model):
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=200)
    neighbourhood = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

class Search(models.Model):
    person = models.ForeignKey(Profile)
    localization = models.ForeignKey(Localization, null=True)
    date = models.DateField(default=datetime.date.today)
    timeBegin = models.TimeField(null=True)
    timeEnd = models.TimeField(null=True)
    sport = models.ManyToManyField(Sport)

class Event(models.Model):
    name = models.CharField(max_length=50)
    creatorProfile = models.ForeignKey(Profile, related_name="creatorProfile", null=True)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    persons = models.ManyToManyField(Profile)
    localization = models.ForeignKey(Localization)
    sport = models.ForeignKey(Sport)
    date = models.DateField(default=datetime.date.today)
    timeBegin = models.TimeField(null=True)
    timeEnd = models.TimeField(null=True)
    description = models.CharField(max_length=2000)
    private = models.BooleanField()
    visible = models.ManyToManyField(Profile, related_name="visible", null=True)


    def getEvent(self, fb_user):
        participants = [(friend.facebook_id, friend.facebook_name, getUserImageUrl(friend.facebook_id)) for friend in self.persons.all()]
        fbFriendsIds = [friend['id'] for friend in fb_user.get_friends()]
        listFriends = []
        listNotFriends = []
        for participant in participants:
            if str(participant[0]) in fbFriendsIds:
                listFriends.append(participant)
            else:
                listNotFriends.append(participant)
        participants = listFriends + listNotFriends
        formattedDate = self.date.strftime("%d/%m")
        formattedTimeBegin = self.timeBegin.strftime("%H:%M")
        price = (Decimal('100') * self.price).quantize(Decimal('1.'))
        return {"name" : self.name, "participants" : participants, "localizationName" : self.localization.name,
                "localizationAddress" : self.localization.adress, "sport" : self.sport.name,
                "friendsCount" : len(listFriends), "date" : formattedDate, "timeBegin" : formattedTimeBegin,
                "id": self.id, "price" : str(price), "private" : self.private, "city" : self.localization.city,
                "neighbourhood" : self.localization.neighbourhood}

    def getDetailedEvent(self, fb_user):
        participants = [(friend.facebook_id, friend.facebook_name, getUserImageUrl(friend.facebook_id)) for friend in self.persons.all()]
        fbFriendsIds = [friend['id'] for friend in fb_user.get_friends()]
        listFriends = []
        listNotFriends = []
        for participant in participants:
            if str(participant[0]) in fbFriendsIds:
                listFriends.append(participant)
            else:
                listNotFriends.append(participant)
        participants = listFriends + listNotFriends
        comments = [(comment.text, comment.person.facebook_name, comment.person.facebook_id, getUserImageUrl(comment.person.facebook_id), str(comment.time), str(comment.day)) for comment in Comment.objects.filter(event=self)]
        formattedDate = self.date.strftime("%d/%m")
        formattedTimeBegin = self.timeBegin.strftime("%H:%M")
        formattedTimeEnd = self.timeEnd.strftime("%H:%M")
        price = (Decimal('100') * self.price).quantize(Decimal('1.'))
        return {"name" : self.name, "participants" : participants, "localizationName" : self.localization.name,
                "localizationAddress" : self.localization.adress, "sport" : self.sport.name, "friendsCount" : len(listFriends),
                "date" : formattedDate, "timeBegin" : formattedTimeBegin, "timeEnd" : formattedTimeEnd,
                "description" : self.description, "comments" : comments, "id": self.id, "price" : str(price),
                "private" : self.private}

class Comment(models.Model):
    event = models.ForeignKey(Event)
    person = models.ForeignKey(Profile)
    text = models.CharField(max_length=2000)
    time = models.TimeField(default=datetime.datetime.now().time())
    day = models.DateField(default=datetime.datetime.today().date())

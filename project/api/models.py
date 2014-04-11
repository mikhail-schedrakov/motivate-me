from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    initial_weight = models.FloatField()
    height = models.FloatField()
    # Relations
    user = models.OneToOneField(User, related_name='profile')


class CheckPoint(models.Model):
    date = models.DateField()
    is_planned = models.BooleanField()
    weight = models.FloatField()
    # Relations
    user = models.ForeignKey(User, related_name='checkpoints')


class Mentor(models.Model):
    email = models.EmailField(max_length=150)
    # Relations
    user = models.ForeignKey(User, related_name='mentors')
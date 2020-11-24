from django.db import models
from django.contrib.auth.models import User
from django import forms
class UserProfileInfo(models.Model):
    user=models.ForeignKey(User,on_delete='PROTECT')

    def __str__(self):
        return self.user.username
class feedback(models.Model):
    name=models.CharField(max_length=250)
    rating=models.CharField(max_length=2)
    text=models.CharField(max_length=250)

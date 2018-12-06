from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Items(models.Model):
    number = models.CharField(max_length=250) #this is a character field and will store sub name
    name = models.CharField(max_length=2000)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    '''when a new subject is created by a user, this function will be called which will redirect
    the user to subject details webpage of the subject we just created using its pk'''
    def get_absolute_url(self):
        return reverse('#', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
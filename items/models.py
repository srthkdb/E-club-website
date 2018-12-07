from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Box(models.Model):
    number = models.CharField(max_length=500) #barcode number
    item = models.CharField(max_length=500) #name of the item in the box(eg. arduino)
    quantity_total = models.IntegerField() #total quantity initially kept in the box
    quantity_left = models.IntegerField() #quantity currently present in the box after issuing and using
    location = models.CharField(max_length=1000) #location where the item is kept is it is not being used or it is not issued

    def __str__(self):
        return self.name


class Issued(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE) #box from which item is issued
    quantity_issued = models.IntegerField() #number of items issued
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user who has the item
    issue_or_use = models.BooleanField(default=False)#if false then using in club, if true then issued
    issue_date = models.DateField(auto_now=True, auto_now_add=True)
    return_date = models.DateField(auto_now=True, auto_now_add=True)
    returned = models.BooleanField(default=False)
    return_number = models.CharField(max_length=500, default='') #barcode number

    '''when a new subject is created by a user, this function will be called which will redirect
    the user to subject details webpage of the subject we just created using its pk'''
    def get_absolute_url(self):
        return reverse('#', kwargs={'pk': self.pk})

    '''def __str__(self):
        return self.name'''
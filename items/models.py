from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    number = models.CharField(max_length=500)
    item = models.CharField(max_length=500)
    quantity_total = models.IntegerField()
    quantity_left = models.IntegerField()
    location = models.CharField(max_length=1000)

    def __str__(self):
        return self.item

class Issued(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    quantity_issued = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    returned = models.BooleanField(default=False)
    return_number = models.CharField(max_length=500, default='')


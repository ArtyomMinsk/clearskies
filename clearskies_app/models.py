from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Airfield(models.Model):
    identifier = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

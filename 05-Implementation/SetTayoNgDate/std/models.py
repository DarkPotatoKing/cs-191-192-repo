from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=256)

class Schedule(models.Model):
    # todo, make foreign keysss
    user_id = models.IntegerField()
    # 0 = Sunday to 6 = Saturday
    day = models.IntegerField()
    # 0 = 00:00 - 00:59 to 23 = 23:00 - 23:99
    hour = models.IntegerField()

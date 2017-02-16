"""
Copyright 2017 Manifold Cheddar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is a course requirement for CS 192 Software Engineering II under the supervision of Asst. Prof. Ma. Rowena C. Solamo of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman for the AY 2016-2017.

"""

#Changelogs:

# 02/01/2017 - Kyle Rosales: Added models

from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.username + ' ' + self.password
        
    @classmethod
    def all(cls):
        return User.objects.all()

    @classmethod
    def authenticate(cls, username, password):
        try:
            user = User.objects.get(username=username)
            return user.password == password
        except:
            return False

    @classmethod
    def create(cls, username, password):
        User(username=username, password=password).save()




class Schedule(models.Model):
    # todo, make foreign keysss
    user_id = models.IntegerField()
    # 0 = Sunday to 6 = Saturday
    day = models.IntegerField()
    # 0 = 00:00 - 00:59 to 23 = 23:00 - 23:99
    hour = models.IntegerField()

    def __str__(self):
        return '{}: {} - {}'.format(self.user_id, self.day, self.hour)

    @classmethod
    def all(cls):
        return Schedule.objects.all()

    @classmethod
    def add_sched(cls, user_id, day, hour):
        Schedule(user_id=user_id, day=day, hour=hour).save()

    @classmethod
    def delete_sched(cls, sched_id):
        sched =  Schedule.objects.get(id=sched_id)
        sched.delete()


class MeetupSchedule(models.Model):
    # todo, make foreign keys
    leader_id = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    start_hour = models.IntegerField()
    start_minute = models.IntegerField()
    end_hour = models.IntegerField()
    end_minute = models.IntegerField()

    def __str__(self):
        return 'leader_id:{} {}/{}/{} {}:{} to {}:{}'.format(self.leader_id, self.date, self.month, self.year, self.start_hour, self.start_minute, self.end_hour, self.end_minute)

    @classmethod
    def all(cls):
        return MeetupSchedule.objects.all()

    @classmethod
    def add_meetup_sched(cls, leader_id, date, month, year, start_hour, start_minute, end_hour, end_minute):
        MeetupSchedule(leader_id=leader_id, date=date, month=month, year=year, start_hour=start_hour, start_minute=start_minute, end_hour=end_hour, end_minute=end_minute).save()

    @classmethod
    def delete_sched(cls, sched_id):
        sched =  MeetupSchedule.objects.get(id=sched_id)
        sched.delete()






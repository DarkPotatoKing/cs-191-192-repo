"""
Copyright 2017 Manifold Cheddar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is a course requirement for CS 192 Software Engineering II under the supervision of Asst. Prof. Ma. Rowena C. Solamo of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman for the AY 2016-2017.

Author: Kyle Rosales

"""

#Changelogs:

# 02/01/2017 - Kyle Rosales: Added models

from __future__ import unicode_literals

from django.db import models

import datetime

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.username + ' ' + self.password + ' ' + self.name

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
    def create(cls, username, password, name):
        User(username=username, password=password, name=name).save()

    # to use this:
    # x = (some User object)
    # x.change_password(old_password, new_password, password_confirm)
    # Returns true if password is changed successfully, false if not
    def change_password(self, old_password, new_password, password_confirm):
        if self.password == old_password and new_password == password_confirm:
            self.password = new_password
            self.save()
            return True
        else:
            return False

class Schedule(models.Model):
    # Schedule is the NOT FREE times
    # todo, make foreign keysss
    user_id = models.IntegerField()
    # 0 = Sunday to 6 = Saturday
    day = models.IntegerField()
    # 1 = 07:00 - 07:30, 2 = 7:30 - 08:00, etc/
    hour = models.IntegerField()

    def __str__(self):
        return 'User#{}: {} - {}'.format(self.user_id, self.day, self.hour)

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

    # use: Schdule.find_common_schedules(user_ids)
    # example, find common schedules of Users with id = 1 and 3
    # Schedule.find_common_schedules([1,3])
    # returns 24x7 matrix (24 30 minute intevals, 7 days)
    # each "cell" in the matrix is a set containing all the ids of users NOT FREE that time
    # blank cells are the common free times of everyone
    @classmethod
    def find_common_schedules(cls, user_ids):
        schedules = filter(lambda x: x.user_id in user_ids, Schedule.all())
        time_table = list()

        for _ in xrange(24):
            x = list()
            for _ in xrange(7):
                x.append(set())
            time_table.append(x)

        for schedule in schedules:
            time_table[schedule.hour - 1][schedule.day].add(schedule.user_id)

        return time_table

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
    description = models.TextField()

    def __str__(self):
        return 'leader_id:{} {}/{}/{} {}:{} to {}:{} "{}"'.format(self.leader_id, self.date, self.month, self.year, self.start_hour, self.start_minute, self.end_hour, self.end_minute, self.description)

    @classmethod
    def all(cls):
        return MeetupSchedule.objects.all()

    @classmethod
    def add_meetup_sched(cls, leader_id, date, month, year, start_hour, start_minute, end_hour, end_minute, description = ''):
        MeetupSchedule(leader_id=leader_id, date=date, month=month, year=year, start_hour=start_hour, start_minute=start_minute, end_hour=end_hour, end_minute=end_minute, description=description).save()

    @classmethod
    def delete_sched(cls, sched_id):
        sched =  MeetupSchedule.objects.get(id=sched_id)
        sched.delete()

    # usage: MeetupSchedule.parse_table(meetup_times)
    # returns day_of_the_week, start_hour, start_minute, end_hour, end_min
    # returns None if invalid
    @classmethod
    def parse_table(cls, meetup_times):
        time_table = list()
        rows = 7
        cols = 24
        days_scheduled = 0
        is_valid = True
        first_true = 0
        last_true = 0
        day_of_the_week = 0

        # 0 to 6 = Sunday to Saturday
        # 1 to 24 = 7 am to 7 pm
        # meetup_times[day][time]

        # create the table
        for _ in xrange(rows):
            time_table.append([False] * cols)

        # add meetup times info to table
        for i in meetup_times:
            day_id = int(i[0])
            time_id = int(i[1]) - 1
            time_table[day_id][time_id] = True

        # check if more than one day of the week is scheduled
        for i in time_table:
            if True in i:
                days_scheduled += 1

        if days_scheduled != 1:
            is_valid = False

        if is_valid:
            for n, i in enumerate(time_table):
                if True in i:
                    day_of_the_week = n
                    first_true = i.index(True)
                    last_true = len(i) - i[::-1].index(True) - 1
                    if i[first_true:last_true+1] == [True] * (last_true - first_true + 1):
                        is_valid = True
                    else:
                        is_valid = False
                    break

        print first_true, last_true
        # first_true, last_true
        # 0 = 7 am, 1 = 7:30 am, ... , 23 = 7 pm
        if is_valid:
            start_hour = 7 + first_true / 2
            start_minute = 30 * (first_true % 2)
            end_hour = 7 + last_true / 2
            end_minute = 30 * (last_true % 2)

            if end_minute == 30:
                end_hour += 1
                end_minute = 0
            else:
                end_minute = 30


        if is_valid:
            return day_of_the_week, start_hour, start_minute, end_hour, end_minute
        else:
            return None

class MeetupRequest(models.Model):
    meetup_schedule_id = models.IntegerField()
    member_id = models.IntegerField()
    is_attending = models.IntegerField(default=0)
    # 0 = No answer, -1 = Not attending, +1 = Attending

    def __str__(self):
        return '(MeetupSched #{}: User#{}, Attending:{})'.format(self.meetup_schedule_id, self.member_id, self.is_attending)

    @classmethod
    def all(cls):
        return MeetupRequest.objects.all()

    @classmethod
    def add_meetup_request(cls, meetup_schedule_id, member_id):
        MeetupRequest(meetup_schedule_id=meetup_schedule_id, member_id=member_id).save()

    @classmethod
    def delete_meetup_request(cls, meetup_request_id):
        MeetupRequest.objects.get(id=meetup_request_id).delete()

    def accept(self):
        self.is_attending = 1
        self.save()
        meetup_schedule = MeetupSchedule.objects.get(id=self.meetup_schedule_id)
        day_of_the_week = datetime.date(meetup_schedule.year, meetup_schedule.month, meetup_schedule.date).isoweekday()

        hour = meetup_schedule.start_hour
        minute = meetup_schedule.start_minute
        end_hour = meetup_schedule.end_hour
        end_minute = meetup_schedule.end_minute

        while not(hour == end_hour and minute == end_minute):
            # def add_sched(cls, user_id, day, hour):
            # 0 = Sunday to 6 = Saturday
            # day = models.IntegerField()
            # 1 = 07:00 - 07:30, 2 = 7:30 - 08:00, etc/
            # hour = models.IntegerField()

            h = 2 * hour - 13
            if minute == 30:
                h += 1

            Schedule.add_sched(self.member_id, day_of_the_week, h)

            if minute == 30:
                minute = 0
                hour += 1
            else:
                minute = 30

    def reject(self):
        self.is_attending = -1
        self.save()

    def get_description(self):
        return MeetupSchedule.objects.get(id=self.meetup_schedule_id).description

    def get_meetup_schedule(self):
        return MeetupSchedule.objects.get(id=self.meetup_schedule_id)

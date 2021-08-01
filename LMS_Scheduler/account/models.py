from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import ModelState
from django.db.models.deletion import Collector
from django.db.models.fields import DateTimeField

# Create your models here.
class Account(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('data published')
    body = models.TextField()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lmsId = models.IntegerField()
    lmsPwd = models.CharField(max_length=45)
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    stamp = models.IntegerField()
    calendarDaystart = models.IntegerField()
    font = models.IntegerField()
    basic = models.IntegerField()
    language = models.IntegerField()

class Attendance(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    attendance=models.DateField()

class Class(models.Model):
    myclass:models.IntegerField()
    class_name=models.CharField(max_length=20)
    class_time=models.TimeField()

class Statistics(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    daily=models.IntegerField()
    date=models.DateField()

class Priority(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    # myclass=models.ForeignKey(Class, on_delete=models.CASCADE)
    # rank=models.IntegerField()
    usertype = models.IntegerField()

class Calendercolor(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Qna(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qna_title=models.CharField(max_length=45)
    qna_date=models.DateTimeField()
    qna_body=models.CharField(max_length=1000)
    qna_answer=models.CharField(max_length=1000)
    qna_view=models.IntegerField()
    def summary(self):
        return self.qna_title[:10]



class Notices(models.Model):
    notice_title=models.CharField(max_length=45)
    notice_date=models.DateTimeField()
    notice_body=models.CharField(max_length=1000)
    notice_view=models.IntegerField()
    def summary(self):
        return self.notice_title[:10]
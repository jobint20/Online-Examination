from django.db import models

# Create your models here.
class exams(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fee = models.CharField(max_length=200)
    timeDuration = models.CharField(max_length=200)
    Type = models.CharField(max_length=200,default="")
    Difficulty = models.CharField(max_length=200,default="")
    

class QPExams(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fee = models.CharField(max_length=200)
    timeDuration = models.CharField(max_length=200)
    rules = models.CharField(max_length=2000000)
    que = models.CharField(max_length=2000000)
    opt1 = models.CharField(max_length=2000000)
    opt2 = models.CharField(max_length=2000000)
    opt3 = models.CharField(max_length=2000000)
    opt4 = models.CharField(max_length=2000000)
    ans = models.CharField(max_length=2000000)
    Type = models.CharField(max_length=200,default="")
    Difficulty = models.CharField(max_length=200,default="")

class examscore(models.Model):
    name = models.CharField(max_length=200)
    fee = models.CharField(max_length=200)
    timeDuration = models.CharField(max_length=200)
    scr = models.CharField(max_length=20)
    username = models.CharField(max_length=200)
    cdate = models.CharField(max_length=200, default="22/04/2021")
    ctime = models.CharField(max_length=200, default="02:50:00")
class payment(models.Model):
    name = models.CharField(max_length=200)
    amount =  models.IntegerField(default=0)
    

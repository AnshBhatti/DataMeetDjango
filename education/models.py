from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class School(models.Model):
    student_first=models.CharField(max_length=20)
    student_last=models.CharField(max_length=20)
    teacher_first=models.CharField(max_length=20,default="")
    teacher_last=models.CharField(max_length=20,default="")
    schoolname=models.CharField(max_length=100,default="")
    confusion=models.IntegerField(default=0)
    happy=models.IntegerField(default=0)
    sad=models.IntegerField(default=0)
    surprised=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    session=models.IntegerField(default=0)
class Teachers(models.Model):
    teacher_name=models.CharField(max_length=41)
    school_name=models.CharField(max_length=100,default="idk")
    sessions=models.IntegerField(default=0)
class Frame(models.Model):
    student_name=models.CharField(max_length=41)
    teacher_name=models.CharField(max_length=41,default="None")
    confusion=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    happy=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    sad=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    surprised=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    image=models.CharField(max_length=1000000)
    timestamp=models.IntegerField(default=0)
class EmotionQueries(models.Model):
    teacher_name=models.CharField(max_length=41)
    school_name=models.CharField(max_length=100)
    confusion=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    happy=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    sad=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    surprised=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    session=models.IntegerField(default=0)
class EmotionQueries1(models.Model):
    teacher_name=models.CharField(max_length=41)
    confusion=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    happy=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    sad=models.DecimalField(default=0,decimal_places=8,max_digits=12)
    surprised=models.DecimalField(default=0,decimal_places=8,max_digits=12)
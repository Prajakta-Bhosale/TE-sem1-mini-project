from django.db import models

# Create your models here.
import datetime

class LoginModel(models.Model):
   Mobile_No = models.CharField(max_length=10)

   def __str__(self):
      return '%s' % self.Mobile_No


class OTPModel(models.Model):
   Enter_OTP=models.CharField(max_length=4)

   def __str__(self):
      return '%s' % self.Enter_OTP
           
       
class EventModel(models.Model):
   # timestamp=datetime.datetime.now()
   EventName=models.CharField(max_length=100)
   SubEventName=models.CharField(max_length=100,null=True)
   EventDate=models.DateField()
   Budget=models.FloatField()
   Description=models.TextField()
   NoOfParticipants=models.PositiveIntegerField()
   Outcomes=models.TextField()
   #images = models.ImageField(upload_to='images/') 
   #images = models.ImageField(upload_to = 'pic_folder/')

   #Photo=models.ImageField(upload_to="gallery")

   def __str__(self):
      return '%s' % self.EventName


class EditModel(models.Model):
   EventName=models.CharField(max_length=100)
   EventDate=models.DateField()
   
   def __str__(self):
      return '%s' % self.EventName
   

class SearchModel(models.Model):
   EventName=models.CharField(max_length=100)
   EventDate=models.DateField()
   
   def __str__(self):
      return '%s' % self.EventName
   
class EventAnalyzeSearchModel(models.Model):
   EventName=models.CharField(max_length=100)
   def __str__(self):
      return '%s' % self.EventName
   

class AnalyzeSearchModel(models.Model):
   EventName=models.CharField(max_length=100)
   SubEventName = models.CharField(max_length=100)
   def __str__(self):
      return '%s' % self.EventName
   
   
class Mails(models.Model):
   email = models.EmailField() 
   subject = models.CharField(max_length=10)
   message = models.TextField()
   document = models.FileField(upload_to='documents/')
   def __str__(self):
      return self.email 
   

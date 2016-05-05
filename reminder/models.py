from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class DoctorProfile(models.Model):
    
    username = models.CharField(max_length=128, unique=True)
    is_doctor = models.BooleanField(default=False)
    num_of_patients = models.IntegerField(default=0)

    def __unicode__(self): 
        return self.username


class PatientProfile(models.Model):
    
    name = models.CharField(max_length=128)
    doctor = models.ForeignKey(DoctorProfile)
    date_of_birth = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=128, null=True)
    cell_phone = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.name

class LogHistory(models.Model):

    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    doctor = models.ForeignKey(DoctorProfile)
    patients = models.CharField(max_length=1024)
    birthday_message = models.BooleanField(default=False)
    subject = models.CharField(max_length=128, null=True)
    message_path = models.CharField(max_length=128, null=True)
    
    def __unicode__(self):
        return self.doctor + " sent a message at " + self.time
        


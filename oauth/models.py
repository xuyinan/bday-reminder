from __future__ import unicode_literals

from django.db import models

# Create your models here.

class OauthUserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    username = models.CharField(max_length=128, unique=True)
    access_token = models.CharField(max_length=128, unique=True)
    refresh_token = models.CharField(max_length=128, unique=True)
    expires_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.username


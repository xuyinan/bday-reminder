#! urs/bin/python

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bthapi.settings')

import django
django.setup()

# For doctor & patient
from reminder.models import DoctorProfile, PatientProfile, LogHistory


doctor = DoctorProfile.objects.get(username='yinanxu')
patients = PatientProfile.objects.filter(doctor=doctor)

for patient in patients:
    patient.email = 'birthdayapi@gmail.com'
    patient.save()


patients = PatientProfile.objects.filter(name='Jenny Harris')
for patient in patients:
    patient.date_of_birth = '1980-09-09'
    patient.email = None
    patient.save()

# For OAuth
from oauth.models import OauthUserProfile


yinanxu = OauthUserProfile.objects.get(username='yinanxu')

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'


if yinanxu:
    yinanxu.access_token = ACCESS_TOKEN
    yinanxu.refresh_token = REFRESH_TOKEN
    yinanxu.expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=172800)
    yinanxu.save()
else:
    OauthUserProfile.objects.create(
            username='yinanxu', 
            access_token='access_token', 
            refresh_token='refresh_token', 
            expires_timestamp=datetime.datetime.now(pytz.utc)
        )


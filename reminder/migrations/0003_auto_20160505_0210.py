# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0002_doctorprofile_loghistory_patientprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loghistory',
            name='message_path',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='loghistory',
            name='subject',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='cell_phone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='date_of_birth',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='email',
            field=models.CharField(max_length=128, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-02 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0016_auto_20170402_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userform',
            name='password',
            field=models.CharField(max_length=80),
        ),
    ]

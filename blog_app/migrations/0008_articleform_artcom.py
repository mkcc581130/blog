# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0007_firstcommentform_secondcommentform'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleform',
            name='artcom',
            field=models.IntegerField(default='0'),
        ),
    ]
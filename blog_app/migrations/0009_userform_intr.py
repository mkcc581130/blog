# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0008_articleform_artcom'),
    ]

    operations = [
        migrations.AddField(
            model_name='userform',
            name='intr',
            field=models.TextField(default='\u5927\u5bb6\u4e00\u8d77\u52a0\u6cb9\uff01'),
        ),
    ]
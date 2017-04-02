# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 09:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_articleform_artread'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirstCommentForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(default='10000')),
                ('artid', models.IntegerField(default='0')),
                ('commenttime', models.DateTimeField(default=django.utils.timezone.now)),
                ('commentcontent', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SecondCommentForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(default='10000')),
                ('artid', models.IntegerField(default='0')),
                ('commenttime', models.DateTimeField(default=django.utils.timezone.now)),
                ('commentcontent', models.TextField()),
                ('replyfirst', models.IntegerField(default='0')),
            ],
        ),
    ]

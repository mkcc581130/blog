# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0014_auto_20170329_1009'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FirstCommentForm',
            new_name='CommentForm',
        ),
        migrations.RenameModel(
            old_name='SecondCommentForm',
            new_name='ReplyForm',
        ),
    ]
# coding:utf8
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# 用户信息表
class UserForm(models.Model):
    userid = models.IntegerField(default='10000')
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=30)
    createIP = models.CharField(max_length=16)
    lastloginIP = models.CharField(max_length=16)
    createtime = models.DateTimeField(default=timezone.now)
    lastlogintime = models.DateTimeField(default=timezone.now)
    userlogo = models.ImageField(upload_to='img_upload', default='img_upload/123_QhgxiJJ.png')
    intr = models.CharField(max_length=70, default='大家一起加油！')

    def __unicode__(self):
        return self.username


# 文章信息表
class ArticleForm(models.Model):
    userid = models.IntegerField(default=10000)
    arttitle = models.CharField(max_length=100)
    artkeyword = models.CharField(max_length=50)
    artcontent = models.TextField()
    artcreatetime = models.DateTimeField(default=timezone.now)
    artlastedittime = models.DateTimeField(default=timezone.now)
    artread = models.IntegerField(default=0)
    artcom = models.IntegerField(default=0)
    artabstract = models.TextField(default='123')
    classify = models.IntegerField(default=4)

    def __unicode__(self):
        return self.arttitle


# 评论信息表
class CommentForm(models.Model):
    userid = models.IntegerField(default='10000')
    artid = models.IntegerField(default='0')
    commenttime = models.DateTimeField(default=timezone.now)
    commentcontent = models.TextField()

    def __unicode__(self):
        return self.commentcontent


# 回复评论信息表
class ReplyForm(models.Model):
    userid = models.IntegerField(default='10000')
    artid = models.IntegerField (default='0')
    commenttime = models.DateTimeField(default=timezone.now)
    commentcontent = models.TextField()
    replyfirst = models.IntegerField(default='0')

    def __unicode__(self):
        return self.commentcontent

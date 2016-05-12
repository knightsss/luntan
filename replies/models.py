#coding=utf-8
from django.db import models

# Create your models here.

class Login(models.Model):
    user_name = models.CharField(max_length=20)
    login_name = models.CharField(max_length=20)    #主键
    pwd = models.CharField(max_length=20)
    power_id = models.IntegerField()
    def __unicode__(self):
        return self.user_name

class Url(models.Model):
    url = models.CharField(max_length=300)
    remark = models.CharField(max_length=200)
    login_name = models.CharField(max_length=20)   #新增字段
    sign = models.CharField(max_length=4)                       #新增字段
    def __unicode__(self):
        return u'%s %s' % (self.url, self.remark)


class Reply(models.Model):
    content = models.CharField(max_length=200)
    login_name = models.CharField(max_length=20)   #新增字段，外键
    sign = models.CharField(max_length=4)                       #新增字段
    def __unicode__(self):
        return self.content

class Ip(models.Model):
    ip = models.CharField(max_length=100)
    port = models.CharField(max_length=100)
    login_name = models.CharField(max_length=20)   #新增字段，外键

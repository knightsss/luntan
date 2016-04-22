from django.db import models

# Create your models here.

class Login(models.Model):
    user_name = models.CharField(max_length=20)
    login_name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    power_id = models.IntegerField()
    def __unicode__(self):
        return self.user_name

class Url(models.Model):
    url = models.CharField(max_length=100)
    remark = models.CharField(max_length=200)
    def __unicode__(self):
        return u'%s %s' % (self.url, self.remark)
class Reply(models.Model):
    content = models.CharField(max_length=200)
    def __unicode__(self):
        return self.content

class Ip(models.Model):
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=10)

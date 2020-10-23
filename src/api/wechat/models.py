from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class WechatUser(models.Model):
    user = models.ForeignKey(User, unique=True)
    nick_name = models.CharField(max_length=255, null=True)
    gender = models.IntegerField(null=True)
    avatar_url = models.URLField(null=True)

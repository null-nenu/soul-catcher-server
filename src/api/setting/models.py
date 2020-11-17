from django.db import models
from uuid import uuid4
import os

# Create your models here.
def get_music_uuid(instance, filename):
    upload_to = 'musics'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def get_image_uuid(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class BackgroundMusic(models.Model):
    file = models.FileField(upload_to=get_music_uuid, null=True)


class BackgroundImage(models.Model):
    file = models.ImageField(upload_to=get_image_uuid, null=True)


class Slogan(models.Model):
    text = models.CharField(max_length=255)


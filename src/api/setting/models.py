from django.db import models

# Create your models here.


class BackgroundMusic(models.Model):
    file = models.FileField(upload_to="musics", null=True)


class BackgroundImage(models.Model):
    file = models.ImageField(upload_to="images", null=True)


class Slogan(models.Model):
    text = models.CharField(max_length=255)

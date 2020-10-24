from django.db import models

# Create your models here.


class BackgroundMusic(models.Model):
    file = models.FileField(null=True)


class BackgroundImage(models.Model):
    file = models.ImageField(null=True)

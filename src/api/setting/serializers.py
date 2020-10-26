from django.db import models
from rest_framework import serializers
from rest_framework import fields
from .models import BackgroundImage, BackgroundMusic, Slogan


class BackgroundMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundMusic
        fields = "__all__"


class BackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundImage
        fields = "__all__"


class SloganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slogan
        fields = "__all__"

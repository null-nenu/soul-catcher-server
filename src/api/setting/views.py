from src.api.scale import serializers
from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BackgroundImage, BackgroundMusic, Slogan
from .serializers import BackgroundImageSerializer, BackgroundMusicSerializer, SloganSerializer
# Create your views here.


class SettingViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["get"])
    def app_config(self, requests):
        image_queryset = BackgroundImage.objects.order_by('?').first()
        music_queryset = BackgroundMusic.objects.order_by('?').first()
        solgan_queryset = Slogan.objects.order_by('?').first()
        image = BackgroundImageSerializer(image_queryset).data
        music = BackgroundMusicSerializer(music_queryset).data
        solgan = SloganSerializer(solgan_queryset).data
        return Response({
            "background": image.get("file"),
            "music": music.get("file"),
            "solgan": solgan.get("text")
        })


class BackgroundMusicViewSet(viewsets.ModelViewSet):
    queryset = BackgroundMusic.objects.all()
    serializer_class = BackgroundMusicSerializer


class BackgroundImageViewSet(viewsets.ModelViewSet):
    queryset = BackgroundImage.objects.all()
    serializer_class = BackgroundImageSerializer


class SloganViewSet(viewsets.ModelViewSet):
    queryset = Slogan.objects.all()
    serializer_class = SloganSerializer

    
    

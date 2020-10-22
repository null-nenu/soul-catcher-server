from django.shortcuts import render
from rest_framework import views

# Create your views here.


class WechatView(views.APIView):
    def create(self, request):
        print(request.data)

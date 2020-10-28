from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from ..scale.models import EvaluationRecord
from ..scale.views import EvaluationRecordSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def destory(self, request):
        userqueryset = User.objects.get(username=request.user)
        user=UserSerializer(userqueryset).data
        EvaluationRecord.objects.filter(user_id=user['id']).update(user=None)
        return Response(status=200)


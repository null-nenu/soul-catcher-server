from django.shortcuts import render
from rest_framework import viewsets
from .models import Evaluation
from .serializers import EvaluationSerializer
# Create your views here.

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
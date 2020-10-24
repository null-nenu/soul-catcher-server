from django.shortcuts import render
from rest_framework import viewsets
from .models import Evaluation
from .models import EvaluationRate
from .models import Question
from .models import Option
from .models import EvaluationRecord
from .models import EvaluationDetail

from .serializers import EvaluationSerializer
from .serializers import EvaluationRateSerializer
from .serializers import QuestionSerializer
from .serializers import OptionSerializer
from .serializers import EvaluationRecordSerializer
from .serializers import EvaluationDetailSerializer


# Create your views here.
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class EvaluationRateViewSet(viewsets.ModelViewSet):
    queryset = EvaluationRate.objects.all()
    serializer_class = EvaluationRateSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class EvaluationRecordViewSet(viewsets.ModelViewSet):
    queryset = EvaluationRecord.objects.all()
    serializer_class = EvaluationRecordSerializer


class EvaluationDetailViewSet(viewsets.ModelViewSet):
    queryset = EvaluationDetail.objects.all()
    serializer_class = EvaluationDetailSerializer

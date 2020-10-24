from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        if pk == None:
            return Response(status=404)
        evaqueryset = Evaluation.objects.get(id=pk)
        evaluation = EvaluationSerializer(evaqueryset, many=False)
        quesqueryset = Question.objects.filter(evaluation_id=pk)
        question = QuestionSerializer(quesqueryset, many=True)
        questiondata = question.data
        for temp in questiondata:
            optionQuerySet = Option.objects.filter(question_id=temp['id'])
            option = OptionSerializer(optionQuerySet, many=True)
            temp['options'] = option.data
        res = dict(evaluation.data)
        res['questions'] = questiondata
        return Response(res)

    @action(methods=['post'], detail=False)
    def score(self,request,pk=None):
        requestdata=request.data
        scoreSum=0
        optionqueryset=Option.objects.filter(question_id__in=requestdata['options'])
        optiondata=QuestionSerializer(optionqueryset,many=True).data
        print(optiondata)
        return Response(optiondata)

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

    @action(methods=['get'], detail=True)
    def details(self,request,pk=None):
        evaratequeryset=EvaluationRate.objects.get(id='1')
        return Response(EvaluationRateSerializer(evaratequeryset,many=False).data)

class EvaluationDetailViewSet(viewsets.ModelViewSet):
    queryset = EvaluationDetail.objects.all()
    serializer_class = EvaluationDetailSerializer

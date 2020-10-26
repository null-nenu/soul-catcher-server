from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime

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
from src.api.user.serializers import UserSerializer

from datetime import datetime


# Create your views here.
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        if pk == None:
            return Response(status=404)
        return Response(evaluationdetails(pk))

    @action(methods=['post'], detail=False)
    def score(self, request, pk=None):
        requestdata = request.data
        scoresum = 0
        optionqueryset = Option.objects.filter(pk__in=requestdata['options'])
        optiondata = OptionSerializer(optionqueryset, many=True).data
        for temp in optiondata:
            scoresum += temp['score']
        # user 临时为none
        user = None
        ftime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[0:-3]
        evaluationrecord = EvaluationRecord(
            user=user, score=scoresum, timestamp=ftime)
        evaluationrecord.evaluation = Evaluation.objects.get(
            id=requestdata['evaluation'])
        evaluationrecord.save()
        recqueryset = EvaluationRecord.objects.filter(
            user=user, evaluation=requestdata['evaluation'], timestamp=ftime)
        rec_id = EvaluationRecordSerializer(
            recqueryset, many=True).data[0]['id']
        savaid = {'id': rec_id}

        for j in requestdata['options']:
            detail_data = EvaluationDetail()
            detail_data.option = Option.objects.get(id=j)
            detail_data.evaluation = evaluationrecord
            detail_data.question = Question.objects.get(
                id=OptionSerializer(detail_data.option).data.get("question"))
            detail_data.save()

        return Response(savaid)


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
    def details(self, request, pk=None):
        evaratequeryset = EvaluationRate.objects.get(id='1')
        return Response(EvaluationRateSerializer(evaratequeryset, many=False).data)

    @action(methods=['get'], detail=False)
    def detailed(self, request):
        
        print(UserSerializer(request.user).data)
        recordqueryset = EvaluationRecord.objects.all()
        recorddata = EvaluationRecordSerializer(recordqueryset, many=True).data
        evaqueryset = Evaluation.objects.all()
        evadata = EvaluationSerializer(evaqueryset, many=True).data
        for temprecord in recorddata:
            for tempeeva in evadata:
                temprecord['timestamp'] = temprecord['timestamp'].replace(
                    'T', ' ').split('.', 1)[0]
                if temprecord['evaluation'] == tempeeva['id']:
                    temprecord['evaluation_name'] = tempeeva['name']
                    temprecord['evaluation_detail'] = tempeeva['detail']
        return Response(recorddata)


class EvaluationDetailViewSet(viewsets.ModelViewSet):
    queryset = EvaluationDetail.objects.all()
    serializer_class = EvaluationDetailSerializer

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        if pk == None:
            return Response(status=404)
        recordqueryset = EvaluationRecord.objects.get(id=pk)
        evaid = EvaluationRecordSerializer(recordqueryset, many=False).data['evaluation']
        evadetailqueryset = EvaluationDetail.objects.filter(evaluation_id=pk)
        evadetaildata = EvaluationDetailSerializer(evadetailqueryset, many=True).data
        selectedoptionid = [o['option'] for o in evadetaildata]
        evadata = evaluationdetails(evaid)
        for tempquestion in evadata['questions']:
            for tempoption in tempquestion['options']:
                if tempoption['id'] in selectedoptionid:
                    tempoption['selected'] = True
                    break
                else:
                    tempoption['selected'] = False
        return Response(evadata)


'''
通过量表Id查询问题和选项
'''


def evaluationdetails(pk):
    evaqueryset = Evaluation.objects.get(id=pk)
    evaluation = EvaluationSerializer(evaqueryset, many=False)
    quesqueryset = Question.objects.filter(evaluation_id=pk)
    question = QuestionSerializer(quesqueryset, many=True)
    questiondata = question.data
    for temp in questiondata:
        optionqueryset = Option.objects.filter(question_id=temp['id'])
        option = OptionSerializer(optionqueryset, many=True)
        temp['options'] = option.data
    res = dict(evaluation.data)
    res['questions'] = questiondata
    return res

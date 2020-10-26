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
from .models import Story

from .serializers import EvaluationSerializer
from .serializers import EvaluationRateSerializer
from .serializers import QuestionSerializer
from .serializers import OptionSerializer
from .serializers import EvaluationRecordSerializer
from .serializers import EvaluationDetailSerializer
from src.api.user.serializers import UserSerializer
from .serializers import StorySerializer

from datetime import datetime


# Create your views here.
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        if pk is None:
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
        evaratequeryset = EvaluationRecord.objects.get(id='1')
        data = {
            "id": 1,
            "timestamp": "2020-10-26 15:28:28",
            "score": 3.0,
            "deleted": 'false',
            "user": 'null',
            "evaluation": 1,
            "level":"轻度抑郁",
            "analysis":"分析你为轻度抑郁，你没救了，等死吧你",
            "advice":"多吃菜少吃饭"
        }
        # return Response(EvaluationRecordSerializer(evaratequeryset, many=False).data)
        return Response(data)

    @action(methods=['get'], detail=False)
    def detailed(self, request):
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

    @action(methods=['get'], detail=False)
    def overview(self, request):
        if request.auth is None:
            return Response({'msg': '未登录'}, status=404)
        data = {'Test': 3, 'Trend': 'normal'}
        return Response(data)


class EvaluationDetailViewSet(viewsets.ModelViewSet):
    queryset = EvaluationDetail.objects.all()
    serializer_class = EvaluationDetailSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    @action(methods=['get'], detail=False)
    def recommend(self, request):
        ID = request.data['id']
        evaluationRecord = EvaluationRecord.objects.get(id=ID)
        score = evaluationRecord.score
        evaluation = evaluationRecord.evaluation
        evaluationRate = EvaluationRate.objects.filter(evaluation=evaluation)
        ERset = EvaluationRateSerializer(evaluationRate, many=True).data
        level = 1
        for temp in ERset:
            if score <= temp['max'] and score >=temp['min']:
                level = temp['level']
                break
            else:
                continue
        data = []
        recommend_query = Story.objects.filter(level=level)
        recommend_data = StorySerializer(recommend_query, many=True).data
        for temp in recommend_data:
            data.append(temp)
        return Response(data)


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

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
import time

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
from .textToPng import textTopng
import uuid
import random

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        return Response(evaluationdetails(pk))


    @action(methods=['post'], detail=False)
    def score(self, request, pk=None):
        begin = datetime.now()
        requestdata = request.data
        scoresum = 0
        optionqueryset = Option.objects.filter(pk__in=requestdata['options'])
        optiondata = OptionSerializer(optionqueryset, many=True).data
        for temp in optiondata:
            scoresum += temp['score']
        user = None
        if request.auth is not None:
            user = User.objects.get(username=request.user)
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
        objs = []

        for j in requestdata['options']:
            detail_data = EvaluationDetail()
            detail_data.option = Option.objects.get(id=j)
            detail_data.evaluation = evaluationrecord
            detail_data.question = Question.objects.get(
                id=OptionSerializer(detail_data.option).data.get("question"))
            objs.append(detail_data)
        EvaluationDetail.objects.bulk_create(objs)
        savaid = {'id': rec_id}
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

    @action(methods=['get'], detail=False)
    def getdetail(self, request):
        ID = request.query_params.get('id')
        evaratequeryset = EvaluationRecord.objects.get(id=ID)
        recorddata = EvaluationRecordSerializer(evaratequeryset, many=False).data
        score = recorddata['score']
        evaluationId = recorddata['evaluation']
        evaluationData = Evaluation.objects.get(id=evaluationId)
        # 表详情
        evaluationTitle = evaluationData.name
        info = evaluationData.detail
        warning = evaluationData.warning
        optionData = evaluationdetails(evaluationId)
        questions = optionData['questions']
        # 选项ID
        detailset = EvaluationDetail.objects.filter(evaluation=ID)
        detail = EvaluationDetailSerializer(detailset, many=True)
        detaildata = detail.data
        optionID = []
        for temp in detaildata:
            optionID.append(temp['option'])

        pngHeight = len(optionID) * 2 +4
        questions = zip(questions, optionID)
        text = ""
        text += evaluationTitle +"\n\n"
        text += info + "\n\n"
        text += warning + "\n\n"
        i = 1
        for item,op in questions:
            text = text + "(" + str(i) + ")、"+ item['content'] + "\n"
            for option in item['options']:
                if option['id'] == op:
                    text = text + "√" + option['content'] + "\n"
                else:
                    text = text + "  " + option['content'] + "\n"
            text = text + "\n"
            i = i + 1
        text += "\n\n本次评测得分为：" + str(score)
        print(text)
        t = time.time()
        filename = str(uuid.uuid1()) + ".png"
        n = textTopng(text, 20, pngHeight, "/var/static/record/" + filename)
        n.draw_text()
        # 未修改
        url = "/static/record/" +  filename
        return Response({"url":url})

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        evaratequeryset = EvaluationRecord.objects.get(id=pk)
        recorddata = EvaluationRecordSerializer(evaratequeryset, many=False).data
        recorddata['timestamp'] = recorddata['timestamp'].replace(
            'T', ' ').split('.', 1)[0]

        ratequeryset = EvaluationRate.objects.filter(evaluation_id=recorddata['evaluation'],
                                                     min__lte=recorddata['score'], max__gte=recorddata['score'])
        ratedata = EvaluationRateSerializer(ratequeryset, many=True).data
        rate = {'level': ratedata[0]['level_text'], 'analysis': ratedata[0]['content'], 'advice': ratedata[0]['advice']}
        recorddata.update(rate)
        return Response(recorddata)

    @action(methods=['get'], detail=False)
    def detailed(self, request):
        userqueryset = User.objects.get(username=request.user)
        user = UserSerializer(userqueryset, many=False).data
        recordqueryset = EvaluationRecord.objects.filter(user_id=user['id'])
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
    
    #总测试次数和趋势
    @action(methods=['get'], detail=False)
    def overview(self, request):
        if request.auth is None:
            return Response({'msg': '未登录'}, status=404)
        userqueryset = User.objects.get(username=request.user)
        user = UserSerializer(userqueryset, many=False).data
        recordqueryset = EvaluationRecord.objects.filter(user=user['id'])
        recorddata = EvaluationRecordSerializer(recordqueryset, many=True).data
        count = len(recorddata)
        trend=''
        if count > 0 :
            ratequeryset = EvaluationRate.objects.filter(evaluation_id=recorddata[-1]['evaluation'],
                                                         min__lte=recorddata[-1]['score'],
                                                         max__gte=recorddata[-1]['score'])
            trend = EvaluationRateSerializer(ratequeryset, many=True).data[0]['level_text']
        return Response({'Test': count, 'Trend': trend})


class EvaluationDetailViewSet(viewsets.ModelViewSet):
    queryset = EvaluationDetail.objects.all()
    serializer_class = EvaluationDetailSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    # 获取测评结果
    @action(methods=['get'], detail=False)
    def recommend(self, request):
        ID = request.query_params.get('id')
        evaluationRecord = EvaluationRecord.objects.get(id=ID)
        score = evaluationRecord.score
        evaluation = evaluationRecord.evaluation
        evaluationRate = EvaluationRate.objects.filter(evaluation=evaluation)
        ERset = EvaluationRateSerializer(evaluationRate, many=True).data
        level = 1
        for temp in ERset:
            if score <= temp['max'] and score >= temp['min']:
                level = temp['level']
                break
            else:
                continue
        # 按level筛选
        data = []
        recommend_query = Story.objects.filter(level=level)
        recommend_data = StorySerializer(recommend_query, many=True).data
        # 随机选择 select_num个 推荐内容
        recommend_len = len(recommend_data)
        select_num = 2
        if recommend_len < 2:
            select_num = recommend_len
        random_list = random.sample(range(recommend_len),select_num);
        for temp in random_list:
            data.append(recommend_data[temp])
        return Response(data)

    def list(self, request):
        queryset = Story.objects.all()
        serializer = StorySerializer(queryset, many=True)
        serializer_data = serializer.data
        data = []
        for item in serializer_data:
            if item['level'] < 4:
                data.append(item)
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


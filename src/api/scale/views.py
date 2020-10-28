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
        user=None
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
        objs=[]

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

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        evaratequeryset = EvaluationRecord.objects.get(id=pk)
        recorddata = EvaluationRecordSerializer(evaratequeryset, many=False).data
        recorddata['timestamp'] = recorddata['timestamp'].replace(
            'T', ' ').split('.', 1)[0]
        recorddata.update(zung(recorddata['score']))
        return Response(recorddata)

    @action(methods=['get'], detail=False)
    def detailed(self, request):
        userqueryset = User.objects.get(username=request.user)
        user=UserSerializer(userqueryset,many=False).data
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

    @action(methods=['get'], detail=False)
    def overview(self, request):
        if request.auth is None:
            return Response({'msg': '未登录'}, status=404)
        userqueryset = User.objects.get(username=request.user)
        user = UserSerializer(userqueryset, many=False).data
        recordqueryset = EvaluationRecord.objects.filter(user=user['id'])
        recorddata = EvaluationRecordSerializer(recordqueryset, many=True).data
        count = len(recorddata)
        score = 0
        for i in recorddata:
            score += i['score']
        score /= count
        trend = zung(score)['level']
        return Response({'Test': count, 'Trend': trend})


class EvaluationDetailViewSet(viewsets.ModelViewSet):
    queryset = EvaluationDetail.objects.all()
    serializer_class = EvaluationDetailSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

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


def zung(score):
    res = {}
    if 0 <= score <= 52:
        res['level'] = '无抑郁'
        res['analysis'] = '你懂得自我调节，不会让情绪一直处于低落、忧郁的状态中。你知道如何应对生活中的事情,' \
                          '即使经历挫折和打击，也一样能够以积极的态度认识并接纳自己，让自己重新获得快乐的体验，' \
                          '在人际交往上，你可以客观的评价自己，不太容易因为他人的评价和态度而怀疑自我。'
        res['advice'] = '开卷有益，多阅读一些心理学、哲学和人文生活类的书籍，' \
                        '可以提高我们的认知水平，帮助我们超越过去的思想局限，培养积极向.上的思维模式。' \
                        '世界.上有很多人和事，他们有的感人，有的则发人深省，多阅读坚强面对困难的人和事，' \
                        '树立信心，相比较之下，我们面对的只是小问题。'

    elif 53 <= score <= 62:
        res['level'] = '轻度抑郁'
        res['analysis'] = '最近，你有时会出现心情低落、不安敏感的情况;有时会觉得注意力很难集中、工作效率也没有以前高，' \
                          '有时又会感到感到精神不济、对外界的好奇心减少。但这些情况出现的频率并不高，多数情况下，' \
                          '你仍可以保持自己的日常生活和工作不被自己的情绪所影响。在某些情况下，' \
                          '你会选择通过和大家说笑的方式来转移自己的注意力，但这个方法并不总是有效，' \
                          '有时反而让你觉得很累，甚至感到更加疲惫。'
        res['advice'] = '负性情绪出现的时候，我们会本能的想要它消失，却又不知从何下手，这种想法会让我们的情绪困扰越来越严重。' \
                        '如果反过来，试着允许自己出面负面情绪，直面他们，反而不安会减少。每- -种情绪，都有好处和坏处。' \
                        '最大化那些好的部分，与坏的部分握手言和，学会从不同的视角看待同- -件事情，说不定你会有新的收获哦!'
    elif 63 <= score <= 72:
        res['level'] = '中度抑郁'
        res['analysis'] = '最近你有时会突然感到心境低落、沮丧，对周围的事情提不起兴趣，' \
                          '懒得与人交往。白天容易感到疲惫，没有办法像以前一样集中注意力，' \
                          '工作和学习上的动力也大不如前；生活无法再给你带来足够的满足感，' \
                          '虽然你还是会用和朋友聚会、吃美食、购物逛街等方式排解情绪，但这些这些方法并不能让你长时间开心起来。'
        res['advice'] = '人在受到情绪困扰的时候，很容易在消极的想法里面沉迷深陷。很多研究证实，在这样的情形下，做冥想会很有帮助。' \
                        '当大脑无法停止转动的时候，把注意力放在身体上，比如摸一下 身边的物体，动动脚趾头，去走一走，' \
                        '或者去做件小事情。目的是，关注你身体的感觉,而借此将注意力放在当下。'
    else:
        res['level'] = '严重抑郁'
        res['analysis'] = '最近你经常感到心境低落、忧郁沮丧，一些看似细微的琐事都能轻易引起你的负面情绪；' \
                          '那些曾经能够令你感到开心、放松的事情，最近似乎都丧失了原有的吸引力，' \
                          '就连与自己最好的朋友相处都觉得是一个负担；你经常感到疲惫、没有活力，' \
                          '注意力也很容易就被分散，工作或学习效率比以前下降了很多，记忆力也大不如以前；' \
                          '晚上无法入睡，白天不愿起床。这种情绪上的困扰已经影响了你的学习、工作及人际交往。'
        res['advice'] = '关注心理健康是一个长期的过程， 如果你尝试了很多办法仍无法改善或减轻你的心理困扰，' \
                        '我们建议你及时寻求专业的心理帮助。你可以在专业心理服务的帮助下，' \
                        '获得心理健康专业评估及情感支持、找到影响你心理健康的原因和改善、解决心理困扰的方法。'
    return res

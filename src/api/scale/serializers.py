from rest_framework import serializers
from rest_framework import fields
from .models import *


class EvaluationSerializer(serializers.Serializer):
    class Meta:
        model = Evaluation
        fields = "__all__"

class EvaluationRateSerializer(serializers.Serializer):
    class Meta:
        model = EvaluationRate
        fields = "__all__"

class QuestionSerializer(serializers.Serializer):
    class Meta:
        model = Question
        fields = "__all__"

class OptionSerializer(serializers.Serializer):
    class Meta:
        model = Option
        fields = "__all__"

class EvaluationRecordSerializer(serializers.Serializer):
    class Meta:
        model = EvaluationRecord
        fields = "__all__"

class EvaluationDetailSerializer(serializers.Serializer):
    class Meta:
        model = EvaluationDetail
        fields = "__all__"

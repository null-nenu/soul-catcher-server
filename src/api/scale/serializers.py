from rest_framework import serializers
from .models import *


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = "__all__"

class EvaluationRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationRate
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"

class EvaluationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationRecord
        fields = "__all__"

class EvaluationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationDetail
        fields = "__all__"

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"
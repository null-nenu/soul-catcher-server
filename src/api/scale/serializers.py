from rest_framework import serializers
from rest_framework import fields
from .models import Evaluation


class EvaluationSerializer(serializers.Serializer):
    class Meta:
        model = Evaluation
        fields = "__all__"

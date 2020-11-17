from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
import uuid
import os


# Create your models here.


class Evaluation(models.Model):
    name = models.CharField(max_length=255, null=True)
    detail = models.TextField(null=True)
    warning = models.TextField(null=True)
    deleted = models.BooleanField(default=False)


class EvaluationRate(models.Model):
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.SET_NULL, null=True)
    min = models.FloatField(null=True)
    max = models.FloatField(null=True)
    level = models.IntegerField(null=True)
    content = models.TextField(null=True)
    advice = models.TextField(null=True)
    deleted = models.BooleanField(default=False)
    level_text = models.CharField(max_length=255, null=True)


class Question(models.Model):
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True)
    deleted = models.BooleanField(default=False)


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True)
    score = models.FloatField(null=True)
    deleted = models.BooleanField(default=False)


class EvaluationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.SET_NULL, null=True)
    score = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_created=True, null=True)
    deleted = models.BooleanField(default=False)


class EvaluationDetail(models.Model):
    evaluation = models.ForeignKey(
        EvaluationRecord, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)


class Story(models.Model):
    level = models.IntegerField(null=True)
    title = models.TextField(null=True)
    markdown = models.TextField(null=True)
    url = models.URLField(null=True)
    type = models.CharField(null=True, max_length=255)
    html = models.TextField(null=True)

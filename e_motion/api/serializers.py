from rest_framework import serializers
from .models import User, Project, LearningModel
from django.contrib.auth.models import User as AuthenticationUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AuthenticationUser
        fields = ['id', 'username', 'password', 'email']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        # fields = '__all__'
        exclude = ('id', 'miou_score', 'top1_score', 'top5_score', 'checkpoint')


class ListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ('id', 'name', 'architecture', 'miou_score', 'top1_score', 'top5_score')


class ListScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ('miou_score', 'top1_score', 'top5_score')

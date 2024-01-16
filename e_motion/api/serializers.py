from rest_framework import serializers
from django.contrib.auth.models import User as AuthenticationUser
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import User, Project, LearningModel


class RequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=AuthenticationUser.objects.all())]
    )
    email = serializers.CharField(
        validators=[EmailValidator(), UniqueValidator(queryset=AuthenticationUser.objects.all())]
    )
    class Meta:
        model = AuthenticationUser
        fields = ['id', 'username', 'password', 'email']
    
    
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

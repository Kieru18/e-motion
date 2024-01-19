"""
Django REST framework serializers module for the 'api' application.

This module defines serializers for converting complex data types, such as Django models,
into Python data types that can be easily rendered into JSON and other content types.
"""

from rest_framework import serializers
from django.contrib.auth.models import User as AuthenticationUser
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Project, LearningModel

class RequestSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration and login data.

    Meta:
        model (AuthenticationUser): The model to be serialized.
        fields (list): The fields to include in the serialization.
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=AuthenticationUser.objects.all())]
    )
    email = serializers.CharField(
        validators=[EmailValidator(), UniqueValidator(queryset=AuthenticationUser.objects.all())]
    )

    class Meta(object):
        model = AuthenticationUser
        fields = ['id', 'username', 'password', 'email']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Project' model.

    Meta:
        model (Project): The model to be serialized.
        fields (list): The fields to include in the serialization.
    """
    class Meta:
        model = Project
        fields = '__all__'


class CreateModelSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new learning model.

    Meta:
        model (LearningModel): The model to be serialized.
        exclude (tuple): The fields to exclude from the serialization.
    """
    class Meta:
        model = LearningModel
        # fields = '__all__'
        exclude = ('id', 'miou_score', 'top1_score', 'top5_score', 'checkpoint')


class ListModelSerializer(serializers.ModelSerializer):
    """
    Serializer for listing learning models with selected attributes.

    Meta:
        model (LearningModel): The model to be serialized.
        fields (tuple): The fields to include in the serialization.
    """
    class Meta:
        model = LearningModel
        fields = ('id', 'name', 'architecture', 'miou_score', 'top1_score', 'top5_score')


class ListScoresSerializer(serializers.ModelSerializer):
    """
    Serializer for listing scores of a learning model.

    Meta:
        model (LearningModel): The model to be serialized.
        fields (tuple): The fields to include in the serialization.
    """
    class Meta:
        model = LearningModel
        fields = ('miou_score', 'top1_score', 'top5_score')

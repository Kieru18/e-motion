from rest_framework import serializers
from .models import User
from django.contrib.auth.models import User as AuthenticationUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AuthenticationUser 
        fields = ['id', 'username', 'password', 'email']

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import UserSerializer, RequestSerializer
from .models import User

from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User as AuthenticationUser

def home(request):
    return HttpResponse('<h1>Hello World!</h1>')


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer

    def post(self, request, format=None):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            username = request.data['username']
            user = AuthenticationUser.objects.get(username=username)
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_200_OK)


class LoginView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer

    def post(self, request, format=None):
        username = request.data['username']
        user = get_object_or_404(AuthenticationUser, username=username)
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = RequestSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})


class TestTokenView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response("passed!")

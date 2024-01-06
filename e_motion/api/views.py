from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework import generics, status, views
from .serializers import UserSerializer, RequestSerializer, ProjectSerializer, ListModelSerializer
from .models import User, Project, LearningModel

from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User as AuthenticationUser


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


class LogoutView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TestTokenView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response("passed!")


class ListProjectsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            content = Project.objects.filter(user=request.user)  # SELECT all User's projects
            serializer = ProjectSerializer(content, many=True)
            return JsonResponse(serializer.data, safe=False)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ListModelsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.user.is_authenticated:
            content = LearningModel.objects.filter(project=request.data["project_id"])  # SELECT all models for the Project
            serializer = ListModelSerializer(content, many=True)
            return JsonResponse(serializer.data, safe=False)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.data
            data['user'] = request.user.id
            serializer = ProjectSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectDeleteView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            project_id = request.data["id"]
            Project.objects.filter(id=project_id).delete()
            return Response({'info': 'Record deleted'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectEditView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            project_id = request.data["id"]
            data = request.data
            data["user"] = request.user.id
            project_instance = Project.objects.get(id=project_id)

            serializer = ProjectSerializer(project_instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'info': 'Record updated'}, status=status.HTTP_202_ACCEPTED)
            return Response({'error': 'Data validation failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class MakePredictionsView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            project_id = request.data["project_id"]
            model_id = request.data["selected_id"]
            # TODO call make_prediction method
            # TODO wynikowy plik z anotacjami w responsie
            return Response({'info': 'JSON ready to download'}, status=status.HTTP_200_OK)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)

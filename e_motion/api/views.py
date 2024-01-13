from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework import generics, status, viewsets, views
from .serializers import UserSerializer, RequestSerializer, ProjectSerializer, \
                         CreateModelSerializer, ListModelSerializer, ListScoresSerializer
from .models import User, Project, LearningModel

from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User as AuthenticationUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from ml.model_endpoint import train, predict
from django.core.exceptions import ValidationError
import imghdr

import json


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
    """
    Handles user logout by deleting the authentication token.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        get(request, format=None): Handles HTTP GET for logging out a user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Handle HTTP GET for logging out a user.

        Deletes the authentication token for the authenticated user.

        Args:
            request (Request): HTTP request object.
            format (str, optional): Requested format. Defaults to None.

        Returns:
            Response: HTTP response indicating success or failure of logout.
        """
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
    """
    Handles listing and creating projects for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        get(request, format=None): Handles HTTP GET for listing the user's projects.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Handle HTTP GET for listing the user's projects.

        Returns a JSON response containing the projects associated with the authenticated user.

        Args:
            request (Request): HTTP request object.
            format (str, optional): Requested format. Defaults to None.

        Returns:
            JsonResponse: JSON response containing user's projects.
        """
        if request.user.is_authenticated:
            content = Project.objects.filter(user=request.user)  # SELECT all User's projects
            serializer = ProjectSerializer(content, many=True)
            return JsonResponse(serializer.data, safe=False)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ListModelsView(generics.ListCreateAPIView):
    """
    Handles listing and creating learning models for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        get(request, *args, **kwargs): Handles HTTP GET for listing models for a specific project.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle HTTP GET for listing models for a specific project.

        Returns a JSON response containing the learning models associated with the specified project.

        Args:
            request (Request): HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments (project_id used here).

        Returns:
            JsonResponse: JSON response containing learning models for the project.
        """
        if request.user.is_authenticated:
            project_id = self.kwargs.get('project_id')
            content = LearningModel.objects.filter(project=project_id)  # SELECT all models for the Project
            serializer = ListModelSerializer(content, many=True)
            return JsonResponse(serializer.data, safe=False)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectCreateView(generics.ListCreateAPIView):
    """
    Handles creating projects for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        post(request, *args, **kwargs): Handles HTTP POST for creating a new project.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle HTTP POST for creating a new project.

        Creates a new project associated with the authenticated user.

        Args:
            request (Request): HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: HTTP response indicating success or failure of project creation.
        """
        if request.user.is_authenticated:
            data = request.data
            data['user'] = request.user.id
            serializer = ProjectSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class UploadAnnotationView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            model_id = self.kwargs.get('model_id')
            file_upload = request.FILES.get('file')

            if file_upload is None:
                return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                storage_path = f'annotations/{model_id}/{file_upload.name}'
                saved_path = default_storage.save(storage_path, file_upload)
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ModelCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.data

            serializer = CreateModelSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                modelId = instance.id
                return Response({'modelId': modelId}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectDeleteView(generics.ListCreateAPIView):
    """
    Handles deleting projects for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        post(request, *args, **kwargs): Handles HTTP POST for deleting a project.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle HTTP POST for deleting a project.

        Deletes the project with the specified ID associated with the authenticated user.

        Args:
            request (Request): HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: HTTP response indicating success or failure of project deletion.
        """
        if request.user.is_authenticated:
            project_id = request.data["id"]
            Project.objects.filter(id=project_id).delete()
            return Response({'info': 'Record deleted'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectEditView(generics.ListCreateAPIView):
    """
    Handles editing projects for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        post(request, *args, **kwargs): Handles HTTP POST for editing a project.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle HTTP POST for editing a project.

        Edits the project with the specified ID associated with the authenticated user.

        Args:
            request (Request): HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: HTTP response indicating success or failure of project editing.
        """
        if request.user.is_authenticated:
            try:
                project_id = request.data["id"]
                data = request.data
                data["user"] = request.user.id
                project_instance = Project.objects.get(id=project_id)
            except Exception:
                return Response({'error': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProjectSerializer(project_instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'info': 'Record updated'}, status=status.HTTP_202_ACCEPTED)
            return Response({'error': 'Data validation failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class ListScoresView(generics.ListCreateAPIView):
    """
    Handles listing scores for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        get(request, *args, **kwargs): Handles HTTP GET for listing scores of a learning model.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle HTTP GET for listing scores of a learning model.

        Returns a JSON response containing scores for the specified learning model.

        Args:
            request (Request): HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: JSON response containing scores for the model.
        """
        if request.user.is_authenticated:
            model_id = self.kwargs.get('model_id')
            content = LearningModel.objects.get(id=model_id)
            serializer = ListScoresSerializer(content)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class UploadFilesView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            project_id = self.kwargs.get('project_id')

            print(request.headers)
            if 'files[]' not in request.FILES:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            files = request.FILES.getlist('files[]')

            uploaded_paths = []
            files_uploaded = 0
            try:
                for file_upload in files:
                    storage_path = f'datasets/{project_id}/{file_upload.name}'
                    file_type = imghdr.what(file_upload)
                    if file_type not in ['jpeg', 'jpg', 'png']:
                        return Response({'error': 'Invalid file format. Only .jpg and .png files are allowed.'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    saved_path = default_storage.save(storage_path, file_upload)
                    files_uploaded += 1
                    uploaded_paths.append(saved_path)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'success': True, 'files_count': files_uploaded, 'paths': uploaded_paths}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class MakePredictionsView(views.APIView):
    """
    Handles making predictions for authenticated users.

    Attributes:
        authentication_classes (list): List of authentication classes (TokenAuthentication).
        permission_classes (list): List of permission classes (IsAuthenticated).

    Methods:
        validate(project_id, model_id): Validates the learning model for the given project.
        get(request, *args, **kwargs): Handles HTTP GET for making predictions.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def validate(self, project_id, model_id):
        """
        Validate the learning model for the given project.

        Args:
            project_id (str): ID of the project.
            model_id (str): ID of the learning model.

        Returns:
            bool: True if the learning model is valid, False otherwise.
        """
        record = LearningModel.objects.get(id=model_id, project_id=project_id)
        if not record:
            return False
        return True

    def get(self, request, *args, **kwargs):
        """
        Handle HTTP GET for making predictions.

        Makes predictions using the specified learning model and project.

        Args:
            request (Request): HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            FileResponse: JSON file response containing the generated annotations.
        """
        if request.user.is_authenticated:
            project_id = kwargs.get('project_id')
            model_id = kwargs.get('model_id')
            if self.validate(project_id, model_id):
                generated_annotations = predict(project_id, model_id)
                json_data = json.dumps(generated_annotations, indent=4)

                response = FileResponse(
                    json_data,
                    as_attachment=True,
                    filename='annotations.json',
                    status=status.HTTP_200_OK,
                )
                return response
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)


class TrainView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            model_id = self.kwargs.get('model_id')
            project_id = LearningModel.objects.get(id=model_id).project.id
            print(f"TrainView project_id: {project_id}, model_id: {model_id}")

            try:
                print("Training started")
                train(project_id, model_id)
                print("Training finished")
                return Response({'success': True}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Authentication error'}, status=status.HTTP_401_UNAUTHORIZED)
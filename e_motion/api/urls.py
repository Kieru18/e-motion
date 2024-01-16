"""
URL patterns for Django API Endpoints.

This module contains URL patterns for mapping API endpoint URLs to the corresponding Django views.

URL Patterns:
    - signup/ (path): Maps to SignUpView for handling user registration.
    - login/ (path): Maps to LoginView for handling user login.
    - logout/ (path): Maps to LogoutView for handling user logout.
    - test_token/ (path): Maps to TestTokenView for testing the validity of the authentication token.
    - list_projects/ (path): Maps to ListProjectsView for listing projects.
    - list_models/<int:project_id>/ (path): Maps to ListModelsView for listing machine learning models for a project.
    - create_project/ (path): Maps to ProjectCreateView for creating projects.
    - delete_project/ (path): Maps to ProjectDeleteView for deleting projects.
    - edit_project/ (path): Maps to ProjectEditView for editing projects.
    - create_model/ (path): Maps to ModelCreateView for creating machine learning models.
    - upload_annotation/<int:model_id>/ (path): Maps to UploadAnnotationView for uploading annotations for a model.
    - make_predictions/<int:project_id>/<int:model_id>/ (path): Maps to MakePredictionsView for making predictions.
    - upload/<int:project_id>/ (path): Maps to UploadFilesView for uploading dataset files for a project.
    - train/<int:model_id>/ (path): Maps to TrainView for triggering the training process for a model.
    - get_scores/<int:model_id>/ (path): Maps to ListScoresView for listing scores of a learning model.
"""

from django.urls import path
from .views import SignUpView, LoginView, LogoutView, TestTokenView, ListProjectsView, \
                   ListModelsView, ProjectCreateView, ProjectDeleteView, ProjectEditView, \
                   MakePredictionsView, UploadFilesView, UploadAnnotationView, ModelCreateView, \
                   TrainView, ListScoresView


urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('test_token', TestTokenView.as_view()),
    path('list_projects', ListProjectsView.as_view()),
    path('list_models/<int:project_id>/', ListModelsView.as_view()),
    path('create_project', ProjectCreateView.as_view()),
    path('delete_project', ProjectDeleteView.as_view()),
    path('edit_project', ProjectEditView.as_view()),
    path('create_model', ModelCreateView.as_view()),
    path('upload_annotation/<int:model_id>/', UploadAnnotationView.as_view()),
    path('make_predictions/<int:project_id>/<int:model_id>/', MakePredictionsView.as_view()),
    path('upload/<int:project_id>/', UploadFilesView.as_view()),
    path('train/<int:model_id>/', TrainView.as_view()),
    path('get_scores/<int:model_id>/', ListScoresView.as_view()),
]

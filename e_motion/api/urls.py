from django.urls import path
from .views import UserView, SignUpView, LoginView, LogoutView, TestTokenView, ListProjectsView, ListModelsView, ProjectCreateView, ProjectDeleteView, ProjectEditView, MakePredictionsView, UploadFilesView, UploadAnnotationView#, ModelCreateView

urlpatterns = [
    # path('users/', UserView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('test_token', TestTokenView.as_view()),
    path('list_projects', ListProjectsView.as_view()),
    path('list_models', ListModelsView.as_view()),
    path('create_project', ProjectCreateView.as_view()),
    path('delete_project', ProjectDeleteView.as_view()),
    path('edit_project', ProjectEditView.as_view()),
    # path('create_model', ModelCreateView.as_view()),
    path('upload_annotation', UploadAnnotationView.as_view())
    path('make_predictions', MakePredictionsView.as_view()),
    path('upload/<int:project_id>/', UploadFilesView.as_view()),
]

from django.urls import path
from .views import UserView, SignUpView, LoginView, LogoutView, TestTokenView, ListProjectsView, ProjectCreateView, ProjectDeleteView, ProjectEditView, UploadFilesView

urlpatterns = [
    # path('users/', UserView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('test_token', TestTokenView.as_view()),
    path('list_projects', ListProjectsView.as_view()),
    path('create_project', ProjectCreateView.as_view()),
    path('delete_project', ProjectDeleteView.as_view()),
    path('edit_project', ProjectEditView.as_view()),
    path('upload/<int:project_id>/', UploadFilesView.as_view(), name='upload_files'),
]

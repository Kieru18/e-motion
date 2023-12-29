from django.urls import path
from .views import UserView, SignUpView, LoginView, TestTokenView, ListProjectsView

urlpatterns = [
    # path('users/', UserView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('test_token', TestTokenView.as_view()),
    path('list_projects', ListProjectsView.as_view()),
]

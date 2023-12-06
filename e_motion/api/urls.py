from django.urls import path
from .views import UserView, home, SignUpView, LoginView, TestTokenView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('', home),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('test_token', TestTokenView.as_view()),
]

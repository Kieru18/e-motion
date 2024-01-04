from django.urls import path
from .views import SignUpView, LoginView, TestTokenView, ListProjectsView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('users/', UserView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('test_token', TestTokenView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list_projects', ListProjectsView.as_view()),
]

from django.urls import path
from .views import UserView, home

urlpatterns = [
    path('users/', UserView.as_view()),
    path('', home)
]
        
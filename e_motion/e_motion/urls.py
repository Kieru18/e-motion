"""
e_motion Project URL Configuration.

This file defines the URL patterns for the e_motion project.

Usage:
    - Admin interface: path('admin/', admin.site.urls)
    - API endpoints: path('api/', include('api.urls'))
    - Frontend views: path('', include('frontend.urls'))

For more details on Django URL patterns, see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('frontend.urls')),
]

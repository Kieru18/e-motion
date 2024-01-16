"""
Django application configuration module for the 'api' application.

This module defines the configuration for the 'api' application, specifying details
such as the default auto field and the name of the application.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Application configuration class for the 'api' application.

    Attributes:
        default_auto_field (str): The default auto field for model definitions.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

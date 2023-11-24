from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, default='X')
    knows_ml = models.BooleanField(null=False, default=False)
    email = models.EmailField(null=False, max_length=254, unique=True)
    password = models.CharField(null=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

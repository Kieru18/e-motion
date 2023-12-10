from django.db import models
from django.contrib.auth.models import User


class LearningModel(models.Model):
    @property
    def model_id(self):
        return self.id
    
    name = models.CharField(null=False, max_length=60)
    hiperparams = models.CharField(null=True, max_length=600)
    checkpoint = models.BinaryField(null=True) 

    class Meta:
        db_table = 'learning_models'


class Project(models.Model):
    @property
    def project_id(self):
        return self.id
    
    title = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=250)
    dataset_url = models.CharField(null=False, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.ForeignKey(LearningModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projects'

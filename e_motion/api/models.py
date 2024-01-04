from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    @property
    def project_id(self):
        return self.id

    title = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=250)
    dataset_url = models.CharField(null=True, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projects'


class LearningModel(models.Model):
    @property
    def model_id(self):
        return self.id

    name = models.CharField(null=False, max_length=60)
    lr = models.FloatField(null=True)
    weight_decay = models.FloatField(null=True)
    epochs = models.PositiveIntegerField(null=True)
    val_set_size = models.FloatField(null=True)
    miou_score = models.FloatField(null=True)
    top1_score = models.FloatField(null=True)
    top5_score = models.FloatField(null=True)
    checkpoint = models.BinaryField(null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'learning_models'

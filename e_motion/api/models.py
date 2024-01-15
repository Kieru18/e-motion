from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    @property
    def project_id(self):
        return self.id

    title = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=250)
    label_studio_project = models.CharField(null=True, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projects'


class LearningModel(models.Model):
    @property
    def model_id(self):
        return self.id

    class Architecture(models.TextChoices):
        FASTER_RCNN = 'Faster RCNN'

    name = models.CharField(null=False, max_length=60)
    architecture = models.CharField(null=False, max_length=60, choices=Architecture.choices,
                                    default=Architecture.FASTER_RCNN)
    learning_rate = models.FloatField(null=True)
    weight_decay = models.FloatField(null=True)
    epochs = models.PositiveIntegerField(null=True)
    validation_set_size = models.IntegerField(null=True)
    miou_score = models.FloatField(null=True, default=None)
    top1_score = models.FloatField(null=True, default=None)
    top5_score = models.FloatField(null=True, default=None)
    checkpoint = models.BinaryField(null=True, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'learning_models'

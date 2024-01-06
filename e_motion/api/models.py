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
    ARCHITECTURE_CHOICES = [
        ('option1', 'Faster RCNN'),
        # ('option2', 'Option 2'),
        # ('option3', 'Option 3'),
        # ('option4', 'Option 4'),
    ]
    architecture = models.CharField(null=False, max_length=60, choices=ARCHITECTURE_CHOICES, default='option1')
    learning_rate = models.FloatField(null=True)
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

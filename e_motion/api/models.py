"""
Django models module for the 'api' application.

This module defines Django models representing data entities related to user projects
and machine learning models.

from django.db import models
from django.contrib.auth.models import User
"""

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Django model representing a user's project.

    Attributes:
        title (CharField): The title of the project.
        description (CharField): The description of the project.
        dataset_url (CharField): The URL of the project's dataset.
        user (ForeignKey): The user associated with the project.

    Methods:
        project_id(): Returns the unique identifier of the project.

    Meta:
        db_table (str): The name of the database table for the 'Project' model.
    """
    
    @property
    def project_id(self):
        """
        Get the unique identifier of the project.

        Returns:
            int: The unique identifier of the project.
        """
        return self.id

    title = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=250)
    dataset_url = models.CharField(null=True, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projects'


class LearningModel(models.Model):
    """
    Django model representing a machine learning model.

    Attributes:
        name (CharField): The name of the model.
        architecture (CharField): The architecture of the model.
        learning_rate (FloatField): The learning rate used in training the model.
        weight_decay (FloatField): The weight decay used in training the model.
        epochs (PositiveIntegerField): The number of training epochs.
        validation_set_size (IntegerField): The size of the validation set.
        miou_score (FloatField): The Mean IoU score achieved by the model.
        top1_score (FloatField): The top-1 accuracy score achieved by the model.
        top5_score (FloatField): The top-5 accuracy score achieved by the model.
        checkpoint (BinaryField): The binary representation of the model's checkpoint.
        project (ForeignKey): The project associated with the model.

    Methods:
        model_id(): Returns the unique identifier of the model.

    Meta:
        db_table (str): The name of the database table for the 'LearningModel' model.
    """
    @property
    def model_id(self):
        """
        Get the unique identifier of the model.

        Returns:
            int: The unique identifier of the model.
        """
        return self.id

    class Architecture(models.TextChoices):
        """
        Enumeration of supported model architectures.
        """
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

# Generated by Django 3.2.20 on 2024-01-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_miuo_score_learningmodel_miou_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='learningmodel',
            old_name='lr',
            new_name='learning_rate',
        ),
        migrations.RenameField(
            model_name='learningmodel',
            old_name='val_set_size',
            new_name='validation_set_size',
        ),
        migrations.AddField(
            model_name='learningmodel',
            name='architecture',
            field=models.CharField(choices=[('option1', 'Faster RCNN')], default='option1', max_length=60),
        ),
    ]

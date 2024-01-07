# Generated by Django 3.2.20 on 2024-01-07 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20240106_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningmodel',
            name='architecture',
            field=models.CharField(choices=[('Faster RCNN', 'Faster Rcnn')], default='Faster RCNN', max_length=60),
        ),
        migrations.AlterField(
            model_name='learningmodel',
            name='checkpoint',
            field=models.BinaryField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='learningmodel',
            name='miou_score',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='learningmodel',
            name='top1_score',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='learningmodel',
            name='top5_score',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='learningmodel',
            name='validation_set_size',
            field=models.IntegerField(null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-15 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_auto_20240107_1948"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="dataset_url",
            new_name="label_studio_project",
        ),
    ]

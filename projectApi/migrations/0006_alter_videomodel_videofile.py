# Generated by Django 4.0.4 on 2022-06-07 05:28

from django.db import migrations, models
import projectApi.models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApi', '0005_usermodel_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='videoFile',
            field=models.FileField(upload_to='Videos', validators=[projectApi.models.file_size]),
        ),
    ]
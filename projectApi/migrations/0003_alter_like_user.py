# Generated by Django 4.0.4 on 2022-05-23 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectApi', '0002_remove_usermodel_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectApi.usermodel'),
        ),
    ]
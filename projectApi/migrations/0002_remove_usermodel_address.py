# Generated by Django 4.0.4 on 2022-05-15 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectApi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='address',
        ),
    ]

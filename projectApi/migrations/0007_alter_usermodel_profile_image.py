# Generated by Django 4.0.4 on 2022-06-09 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApi', '0006_alter_videomodel_videofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='profile_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile/'),
        ),
    ]

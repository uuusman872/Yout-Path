# Generated by Django 4.0.4 on 2022-06-03 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApi', '0004_videomodel_videothumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]

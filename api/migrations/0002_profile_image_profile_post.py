# Generated by Django 5.1.4 on 2024-12-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='post',
            field=models.TextField(blank=True, null=True),
        ),
    ]

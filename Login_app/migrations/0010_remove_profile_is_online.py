# Generated by Django 3.1.2 on 2020-11-26 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login_app', '0009_profile_is_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_online',
        ),
    ]
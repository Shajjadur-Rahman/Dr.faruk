# Generated by Django 3.1.2 on 2020-11-24 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login_app', '0002_loginlogoutlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginlogoutlog',
            name='session_key',
        ),
    ]

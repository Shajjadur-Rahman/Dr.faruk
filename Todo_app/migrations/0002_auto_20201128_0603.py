# Generated by Django 3.1.2 on 2020-11-28 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-task_start']},
        ),
    ]

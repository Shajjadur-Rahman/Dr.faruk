# Generated by Django 3.1.2 on 2020-11-24 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login_app', '0003_remove_loginlogoutlog_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginlogoutlog',
            name='host',
        ),
        migrations.AlterField(
            model_name='loginlogoutlog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

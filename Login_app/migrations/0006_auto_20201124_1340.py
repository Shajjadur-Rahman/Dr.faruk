# Generated by Django 3.1.2 on 2020-11-24 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login_app', '0005_auto_20201124_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginlogoutlog',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-24 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login_app', '0004_auto_20201124_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginlogoutlog',
            name='log_out',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loginlogoutlog',
            name='login',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

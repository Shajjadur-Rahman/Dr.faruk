# Generated by Django 3.1.2 on 2020-11-26 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Message_app', '0002_auto_20201124_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='active',
            new_name='new_msg_active',
        ),
    ]
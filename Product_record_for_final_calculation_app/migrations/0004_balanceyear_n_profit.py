# Generated by Django 3.1.2 on 2020-11-23 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_record_for_final_calculation_app', '0003_auto_20201123_0222'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanceyear',
            name='n_profit',
            field=models.FloatField(default=0.0),
        ),
    ]
# Generated by Django 3.1.2 on 2020-11-22 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product_record_for_final_calculation_app', '0002_expense_invoice_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balancesheet',
            name='closing_balance',
        ),
        migrations.RemoveField(
            model_name='balancesheet',
            name='total_profit',
        ),
    ]

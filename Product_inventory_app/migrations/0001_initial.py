# Generated by Django 3.1.2 on 2020-11-21 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.PositiveIntegerField(unique=True)),
                ('import_expense_type', models.CharField(max_length=200)),
                ('expense_amount', models.FloatField()),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('created_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-invoice_no'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250, unique=True)),
                ('product_no', models.PositiveIntegerField(default=0, unique=True)),
                ('rate', models.FloatField()),
                ('quantity', models.PositiveIntegerField()),
                ('qty_for_avg', models.PositiveIntegerField()),
                ('unit_tag', models.CharField(max_length=200)),
                ('total_price', models.FloatField()),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product_inventory_app.importinvoice')),
            ],
            options={
                'ordering': ['-product_no'],
            },
        ),
        migrations.CreateModel(
            name='StockHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250)),
                ('product_no', models.PositiveIntegerField(default=0)),
                ('rate', models.FloatField(default=0.0)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_tag', models.CharField(max_length=200)),
                ('total_price', models.FloatField()),
                ('supplier', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('import_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product_inventory_app.stock')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product_inventory_app.importinvoice')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BackUpData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_no', models.PositiveIntegerField(default=0, unique=True)),
                ('rate', models.FloatField()),
                ('qty_for_avg', models.PositiveIntegerField()),
                ('total_price', models.FloatField()),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product_inventory_app.stock')),
            ],
        ),
    ]

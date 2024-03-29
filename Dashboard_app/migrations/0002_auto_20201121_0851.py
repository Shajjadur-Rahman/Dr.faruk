# Generated by Django 3.1.2 on 2020-11-21 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product_inventory_app', '0001_initial'),
        ('Dashboard_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shadeno',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='Dashboard_app.customer'),
        ),
        migrations.AddField(
            model_name='product',
            name='select_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product_inventory_app.stock'),
        ),
        migrations.AddField(
            model_name='product',
            name='shade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Dashboard_app.shadeno'),
        ),
        migrations.AddField(
            model_name='product',
            name='sold_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentcart',
            name='customers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='Dashboard_app.customer'),
        ),
        migrations.AddField(
            model_name='paymentcart',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='Dashboard_app.product'),
        ),
        migrations.AddField(
            model_name='paymentcart',
            name='shade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Dashboard_app.shadeno'),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('phone',)},
        ),
    ]

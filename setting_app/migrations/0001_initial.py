# Generated by Django 3.1.2 on 2020-11-21 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('keyword', models.CharField(blank=True, max_length=500, null=True)),
                ('company', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_info', models.TextField(blank=True, null=True)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='logo')),
                ('company_logo_text', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=60, null=True)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('facebook', models.URLField(blank=True, max_length=300, null=True)),
                ('youtube', models.URLField(blank=True, max_length=300, null=True)),
                ('twitter', models.URLField(blank=True, max_length=300, null=True)),
                ('instagram', models.URLField(blank=True, max_length=300, null=True)),
                ('linkedin', models.URLField(blank=True, max_length=300, null=True)),
                ('google_plus', models.URLField(blank=True, max_length=300, null=True)),
                ('smtpserver', models.CharField(blank=True, max_length=50, null=True)),
                ('smtpemail', models.EmailField(blank=True, max_length=250, null=True)),
                ('smtppassword', models.CharField(blank=True, max_length=250, null=True)),
                ('smtpport', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('True', 'True'), ('False', 'False')], default='True', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

# Generated by Django 5.0 on 2024-01-02 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0002_device_catogry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeldevice',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

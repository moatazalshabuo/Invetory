# Generated by Django 5.0 on 2024-01-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0008_device_warranty_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicefile',
            name='file',
            field=models.FileField(upload_to='file/%d'),
        ),
    ]

# Generated by Django 5.0 on 2024-01-04 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0007_device_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='Warranty_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
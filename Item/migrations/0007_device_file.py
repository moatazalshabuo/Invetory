# Generated by Django 5.0 on 2024-01-03 12:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0006_devicefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Item.devicefile'),
        ),
    ]

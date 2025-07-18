# Generated by Django 5.2 on 2025-05-08 09:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created_by',
            field=models.CharField(editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='blog',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]

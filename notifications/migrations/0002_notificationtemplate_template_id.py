# Generated by Django 5.2 on 2025-04-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationtemplate',
            name='template_id',
            field=models.CharField(blank=True, help_text='Template ID from Edumarc SMS', max_length=100),
        ),
    ]

# Generated by Django 5.2 on 2025-05-20 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_options_alter_eventcategory_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='map_embed_url',
        ),
    ]

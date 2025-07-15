from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_alter_blog_content_alter_blog_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='published_date',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='created_time',
        ),
    ]
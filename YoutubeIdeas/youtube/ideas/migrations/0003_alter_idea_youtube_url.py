# Generated by Django 5.1.3 on 2024-11-18 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_alter_idea_youtube_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='youtube_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

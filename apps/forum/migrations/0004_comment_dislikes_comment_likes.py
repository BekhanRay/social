# Generated by Django 5.0.4 on 2024-06-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 4.2.3 on 2024-07-14 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_customuser_confirmation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='content',
        ),
    ]
# Generated by Django 5.0.4 on 2024-06-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='education_profession',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='general_info',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='habits_preferences',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='personal_info',
            field=models.TextField(default=''),
        ),
    ]
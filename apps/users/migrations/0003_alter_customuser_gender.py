# Generated by Django 5.0.4 on 2024-06-18 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_photo_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('парень', 'Парень'), ('девушка', 'Девушка')], max_length=7),
        ),
    ]
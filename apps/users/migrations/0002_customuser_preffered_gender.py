# Generated by Django 4.2.3 on 2024-06-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='preffered_gender',
            field=models.CharField(choices=[('мужской', 'Мужской'), ('женский', 'Женский')], default='Все', max_length=7),
        ),
    ]

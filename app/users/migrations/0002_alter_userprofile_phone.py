# Generated by Django 5.1.2 on 2024-10-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=32, verbose_name='Номер телефона'),
        ),
    ]
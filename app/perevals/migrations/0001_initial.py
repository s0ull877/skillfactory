# Generated by Django 5.1.2 on 2024-10-26 16:37

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)], verbose_name='Широта')),
                ('longitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)], verbose_name='Длина')),
                ('height', models.IntegerField(verbose_name='Высота')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(choices=[('', None), ('1A', '1A'), ('1B', '1B'), ('2A', '2A'), ('2B', '2B'), ('3A', '3A'), ('3B', '3B')], max_length=2, null=True, verbose_name='Тяжесть пути зимой')),
                ('summer', models.CharField(choices=[('', None), ('1A', '1A'), ('1B', '1B'), ('2A', '2A'), ('2B', '2B'), ('3A', '3A'), ('3B', '3B')], max_length=2, null=True, verbose_name='Тяжесть пути летом')),
                ('autumn', models.CharField(choices=[('', None), ('1A', '1A'), ('1B', '1B'), ('2A', '2A'), ('2B', '2B'), ('3A', '3A'), ('3B', '3B')], max_length=2, null=True, verbose_name='Тяжесть пути осенью')),
                ('spring', models.CharField(choices=[('', None), ('1A', '1A'), ('1B', '1B'), ('2A', '2A'), ('2B', '2B'), ('3A', '3A'), ('3B', '3B')], max_length=2, null=True, verbose_name='Тяжесть пути весной')),
            ],
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(verbose_name='Заголовок')),
                ('title', models.CharField(verbose_name='Название')),
                ('other_titles', models.CharField(verbose_name='Доп. название')),
                ('connect', models.CharField(blank=True, max_length=4, null=True, verbose_name='Что соединяет, текстовое поле')),
                ('add_time', models.DateTimeField(verbose_name='Дата добавления пользователем')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('coords', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='perevals.coordinates', verbose_name='Координаты перевала')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile', verbose_name='Добавил пользователь')),
                ('level', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='perevals.perevallevel', verbose_name='Сложность во времена года')),
            ],
            options={
                'db_table': 'pereval_added',
            },
        ),
        migrations.CreateModel(
            name='PerevalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='Описание к фотографии')),
                ('image', models.ImageField(upload_to='perevals_images/', verbose_name='Изображение')),
                ('to_pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='perevals.pereval', verbose_name='Перевал')),
            ],
        ),
    ]

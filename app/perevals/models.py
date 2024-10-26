from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import UserProfile


class PerevalLevel(models.Model):

    CHOICES=(
        ('1A', '1A'),
        ('1B', '1B'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('3A', '3A'),
        ('3B', '3B'),
    )

    winter=models.CharField(
        verbose_name="Тяжесть пути зимой", 
        max_length=2, 
        choices=CHOICES,
        null=True)
    summer=models.CharField(
        verbose_name="Тяжесть пути летом", 
        max_length=2,
        choices=CHOICES,
        null=True)
    autumn=models.CharField(
        verbose_name="Тяжесть пути осенью", 
        max_length=2,
        choices=CHOICES,
        null=True)
    spring=models.CharField(
        verbose_name="Тяжесть пути весной", 
        max_length=2,
        choices=CHOICES,
        null=True)

class Coordinates(models.Model):

    latitude=models.FloatField(
        verbose_name='Широта',
        validators=[
            MaxValueValidator(90),
            MinValueValidator(-90)
        ])
    longitude=models.FloatField(
        verbose_name='Длина',
        validators=[
            MaxValueValidator(180),
            MinValueValidator(-180)
        ])
    height=models.IntegerField(verbose_name='Высота')

    def __str__(self) -> str:
        return f'{self.latitude} {self.longitude} {self.height}'


class Pereval(models.Model):

    beauty_title=models.CharField(
        verbose_name='Загаловок'
    )
    title=models.CharField(
        verbose_name='Название'
    )
    other_titles=models.CharField(
        verbose_name='Доп. название'
    )
    connect=models.CharField(
        verbose_name="Что соединяет, текстовое поле",
        max_length=4, blank=True,
        null=True
    )
    add_time=models.DateTimeField(
        verbose_name='Дата добавления пользователем'
    )
    user = models.OneToOneField(
        to=UserProfile, on_delete=models.CASCADE,
        verbose_name='Добавил пользователь'
    )
    coords = models.OneToOneField(
        to=Coordinates, on_delete=models.PROTECT,
        verbose_name='Координаты перевала'
    )
    level = models.OneToOneField(
        to=PerevalLevel, on_delete=models.PROTECT,
        verbose_name='Сложность во времена года'
    )

    

    def __str__(self) -> str:
        return f'{self.beautyTitle} {self.title} | {self.user}'

    class Meta:

        db_table = 'pereval_added'


class PerevalImage(models.Model):

    to_pereval=models.ForeignKey(
        to=Pereval, on_delete=models.CASCADE,
        verbose_name='Перевал',
        related_name='images')
    title=models.CharField(
        verbose_name='Описание к фотографии')
    image = models.ImageField(
        upload_to='perevals_images/',
        verbose_name='Изображение')

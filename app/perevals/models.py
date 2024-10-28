import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from app.settings import MEDIA_ROOT
from users.models import UserProfile
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver



class PerevalLevel(models.Model):

    CHOICES=(
        ("", None,),
        ('1A', '1A',),
        ('1B', '1B',),
        ('2A', '2A',),
        ('2B', '2B',),
        ('3A', '3A',),
        ('3B', '3B',),
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

    CHOICES = (
        ('new', 'new',),
        ('pending', 'pending',),
        ('accepted', 'accepted',),
        ('rejected', 'rejected',),
    )

    beauty_title=models.CharField(
        verbose_name='Заголовок'
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
    user = models.ForeignKey(
        to=UserProfile, on_delete=models.CASCADE,
        verbose_name='Добавил пользователь'
    )
    coords = models.OneToOneField(
        to=Coordinates, on_delete=models.SET_NULL,
        verbose_name='Координаты перевала', null=True
    )
    level = models.OneToOneField(
        to=PerevalLevel, on_delete=models.SET_NULL,
        verbose_name='Сложность во времена года',
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True, editable=False
    )
    status = models.CharField(
        verbose_name='Статус модерации',
        choices=CHOICES, max_length=8,
        default='new', blank=True
    )

    def __str__(self) -> str:
        return f'{self.connect}'.join([self.beauty_title, self.title, self.other_titles])

    class Meta:

        db_table = 'pereval_added'


@receiver(pre_delete, sender=Pereval)
def delete_related_fields(sender, instance, using, **kwargs):
    try:
        instance.coords.delete()
    except AttributeError:
        pass
    try:
        instance.level.delete()
    except AttributeError:
        pass


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

@receiver(post_delete, sender=PerevalImage)
def delete_related_fields(sender, instance, using, **kwargs):

    path = MEDIA_ROOT / instance.image.name
    os.remove(path)

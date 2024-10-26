from django.db import models

# если понадобиться регистрация и авторизация пользователя
# данный класс будет как поле profile auth.User
class UserProfile(models.Model):

    name = models.CharField(
        max_length=32,
        verbose_name='Имя пользователя')
    fam = models.CharField(
        max_length=32,
        verbose_name='Фамилия пользователя')
    otc = models.CharField(
        max_length=32,
        blank=True, null=True,
        verbose_name='Отчество пользователя')
    phone=models.CharField(
        verbose_name='Номер телефона', 
        max_length=32)
    email=models.EmailField(
        verbose_name='Эл. почта',
        unique=True)


    @property
    def full_name(self):

        return f'{self.name} {self.fam} {self.otc}'

    def __str__(self):
        return f'{self.email} | {self.full_name}'
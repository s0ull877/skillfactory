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
    oct = models.CharField(
        max_length=32,
        blank=True, null=True,
        verbose_name='Отчество пользователя')
    phone=models.CharField(
        verbose_name='Номер телефона', 
        max_length=15)
    email=models.EmailField(
        verbose_name='Эл. почта',
        unique=True)


    def full_name(self):

        return f'{self.name} {self.fam} {self.otc}'

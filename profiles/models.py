from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'profile'):
            profile = Profile(user=self)
            profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    forename = models.CharField('Имя', max_length=255, blank=True)
    surname = models.CharField('Фамилия', max_length=255, blank=True)
    patronymic = models.CharField('Отчество', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль - {self.user.username}'

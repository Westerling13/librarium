import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class AutoDateModel(models.Model):
    dt_created = models.DateTimeField('Дата создания', auto_now_add=True)
    dt_updated = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True


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


class Profile(AutoDateModel):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    forename = models.CharField('Имя', max_length=255, blank=True)
    surname = models.CharField('Фамилия', max_length=255, blank=True)
    patronymic = models.CharField('Отчество', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль - {self.user.username}'


def get_return_date():
    return datetime.datetime.now().date() + settings.READING_TIMEDELTA


class LibraryRecord(AutoDateModel):
    READING = 'reading'
    FINISHED = 'finished'
    STATUS_CHOICES = (
        (READING, 'Сейчас читаю'),
        (FINISHED, 'Прочитаны'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='library_records',
    )
    book = models.ForeignKey(
        'bookstore.Book',
        verbose_name='Книга',
        on_delete=models.PROTECT,
        related_name='library_records',
    )
    status = models.CharField('Статус', choices=STATUS_CHOICES, default=READING, max_length=255)
    dt_return = models.DateField('Дата возврата книги', default=get_return_date)

    class Meta:
        verbose_name = 'Библиотечная запись'
        verbose_name_plural = 'Библиотечные записи'

    def __str__(self):
        return f'Библиотечная запись#{self.id}'

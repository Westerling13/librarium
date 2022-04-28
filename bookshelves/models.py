from django.db import models

from profiles.models import AutoDateModel
from profiles.user import User


class UserBook(AutoDateModel):
    READING = 'reading'
    STATUS_CHOICES = (
        (READING, 'Сейчас читаю'),
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    book = models.ForeignKey('bookstore.Book', verbose_name='Книга', on_delete=models.PROTECT)
    status = models.CharField('Статус книги', choices=STATUS_CHOICES, default=READING, max_length=255)

    class Meta:
        verbose_name = 'Книга пользователя'
        verbose_name_plural = 'Книги пользователей'

    def __str__(self):
        return f'Книга пользователя#{self.id}'

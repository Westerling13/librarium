from django.db import models

from profiles.models import AutoDateModel


class Author(AutoDateModel):
    forename = models.CharField('Имя', max_length=255)
    surname = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.short_name

    @property
    def short_name(self):
        name = f'{self.surname} {self.forename[0]}.'
        if self.patronymic:
            name += f' {self.patronymic[0]}.'
        return name


class Book(AutoDateModel):
    author = models.ManyToManyField('Author', verbose_name='Авторы', related_name='authors')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', max_length=1000, blank=True)
    dt_release = models.DateField('Дата выхода')
    category = models.ManyToManyField('Category', verbose_name='Категории', related_name='categories')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Category(AutoDateModel):
    title = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

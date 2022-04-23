from django.db import models

from profiles.models import AutoDateModel


class AuthorQuerySet(models.QuerySet):
    def short_names(self):
        short_names = []
        for author in self.all():
            short_names.append(author.short_name)
        return short_names


class Author(AutoDateModel):
    forename = models.CharField('Имя', max_length=255)
    surname = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255, blank=True)

    objects = AuthorQuerySet.as_manager()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.short_name

    @property
    def short_name(self):
        name = f'{self.surname} {self.forename[0]}.'
        if self.patronymic:
            name += f'{self.patronymic[0]}.'
        return name


class Book(AutoDateModel):
    authors = models.ManyToManyField('Author', verbose_name='Авторы')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', max_length=1000, blank=True)
    dt_release = models.DateField('Дата выхода')
    categories = models.ManyToManyField('Category', verbose_name='Категории')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Section(AutoDateModel):
    DEFAULT_SECTION = 'Без раздела'

    title = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return f'{self.title}'


class Category(AutoDateModel):
    DEFAULT_TITLE = 'Без категории'
    
    title = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'

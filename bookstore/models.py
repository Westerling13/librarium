from django.core.validators import MinValueValidator
from django.db import models

from profiles.models import AutoDateModel
from profiles.user import User


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
    cover = models.ImageField('Обложка', upload_to='bookstore/covers/', null=True, blank=True)
    publication_year = models.PositiveSmallIntegerField('Год издания', validators=[MinValueValidator(1900)], null=True)
    edition = models.PositiveSmallIntegerField('Номер издания', null=True)
    section = models.ForeignKey(
        'BookSection',
        verbose_name='Книжный раздел',
        related_name='books',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    free_copies_number = models.PositiveIntegerField('Количество свободных экземпляров', default=1)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class BookSection(AutoDateModel):
    title = models.CharField('Название', max_length=255)
    number = models.PositiveIntegerField('Номер раздела', unique=True)

    class Meta:
        verbose_name = 'Книжный раздел'
        verbose_name_plural = 'Книжные разделы'

    def __str__(self):
        return f'{self.title}'


class BookReadingRecord(AutoDateModel):
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
        related_name='book_reading_records',
    )
    book = models.ForeignKey(
        'bookstore.Book',
        verbose_name='Книга',
        on_delete=models.PROTECT,
        related_name='reading_records',
    )
    status = models.CharField('Статус', choices=STATUS_CHOICES, default=READING, max_length=255)

    class Meta:
        verbose_name = 'Запись чтения книги'
        verbose_name_plural = 'Записи чтения книг'

    def __str__(self):
        return f'Запись чтения книги#{self.id}'

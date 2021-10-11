# Generated by Django 3.2.8 on 2021-10-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('dt_updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('forename', models.CharField(max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=255, verbose_name='Отчество')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('dt_updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
                ('dt_release', models.DateField(verbose_name='Дата выхода')),
                ('author', models.ManyToManyField(related_name='authors', to='bookstore.Author', verbose_name='Авторы')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
    ]

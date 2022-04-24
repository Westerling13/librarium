# Generated by Django 3.2.13 on 2022-04-24 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0007_book_free_copies_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksection',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Номер раздела'),
        ),
    ]

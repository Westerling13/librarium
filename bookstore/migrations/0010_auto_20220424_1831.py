# Generated by Django 3.2.13 on 2022-04-24 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0009_alter_booksection_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Номер издания'),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1900)], verbose_name='Год издания'),
        ),
    ]

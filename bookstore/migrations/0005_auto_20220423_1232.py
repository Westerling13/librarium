# Generated by Django 3.2.13 on 2022-04-23 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_auto_20220423_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]

# Generated by Django 3.1.6 on 2021-03-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0017_auto_20210312_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(allow_unicode=True, help_text='Идентификатор рецепта', unique=True, verbose_name='Идентификатор рецепта'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-03-12 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0016_auto_20210312_1938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='quantityofingredient',
            options={'verbose_name_plural': 'Количество ингредиентов'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, help_text='Название ингредиента', max_length=200, verbose_name='Ингредиент'),
        ),
    ]

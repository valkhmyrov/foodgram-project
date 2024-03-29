# Generated by Django 3.1.6 on 2021-03-06 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodgram', '0012_shoplist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name_plural': 'Список избранного'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['user', 'author'], 'verbose_name_plural': 'Подписка на авторов'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.AlterModelOptions(
            name='quantityofingredient',
            options={'verbose_name_plural': 'Количество ингридиентов'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='shoplist',
            options={'verbose_name_plural': 'Список покупок'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['pk'], 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации'),
        ),
        migrations.AlterField(
            model_name='shoplist',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='foodgram.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoplist',
            name='user',
            field=models.ForeignKey(help_text='Покупатель', on_delete=django.db.models.deletion.CASCADE, related_name='shop_list', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='checkbox_style',
            field=models.CharField(max_length=30, verbose_name='Цвет чекбокса'),
        ),
    ]

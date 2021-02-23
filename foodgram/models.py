from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db.models.deletion import CASCADE


User = get_user_model()


class Tag(models.Model):
    MEAL = (
        ('B', 'Завтрак'),
        ('D', 'Обед'),
        ('S', 'Ужин')
    )
    tag = models.CharField(max_length=1, choices=MEAL)

    def __str__(self):
        return self.get_tag_display()


class Ingredient(models.Model):
    name = models.CharField('Ингридиент', db_index=True, max_length=200, help_text='Название ингридиента')
    dimension = models.CharField('Единица измерения', db_index=True, max_length=200, help_text='Единица измерения')

    def __str__(self):
        return self.name[0:30]


class Recipe(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='recipes', help_text='Автор')
    title = models.CharField('Заголовок', db_index=True, max_length=200, help_text='Название')
    image = models.ImageField('Изображение', upload_to='foodgram_images/', help_text='Изображение')
    text = models.TextField('Текст рецепта', help_text='Текст рецепта')
    ingredients = models.ManyToManyField(Ingredient, through='QuantityOfIngredient')
    tag = models.ManyToManyField(Tag, verbose_name='Тег', related_name='Recipe')
    time = models.IntegerField('Время приготовления', validators=[MaxValueValidator(1440)], help_text='Время приготовления')
    slug = models.SlugField(unique=True, help_text='Идентификатор рецепта')

    def __str__(self):
        return self.title[0:30]


class QuantityOfIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    quantity = models.IntegerField('Количество', help_text='Количество')
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.deletion import CASCADE


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=30, verbose_name='Наименование тега', unique=True)
    checkbox_style = models.CharField(max_length=30)

    #class Meta:
    #    verbose_name = 'тег'
    #    verbose_name_plural = 'теги'

    def __str__(self):
        return self.title[0:15]


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
    tags = models.ManyToManyField(Tag, verbose_name='Тег', related_name='Recipe')
    time = models.IntegerField('Время приготовления', validators=[MaxValueValidator(1440)], help_text='Время приготовления')
    slug = models.SlugField(unique=True, help_text='Идентификатор рецепта')
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[0:30]


class QuantityOfIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    quantity = models.IntegerField('Количество', help_text='Количество')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', help_text='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', help_text='Публицист')

    class Meta:
        ordering = ['user', 'author']
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique together'),
            ]
            
    def __str__(self):
        user = self.user.username
        author = self.author.username
        output = f'user: {user}, author: {author}'
        return output

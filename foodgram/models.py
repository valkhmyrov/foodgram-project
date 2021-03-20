from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models import Exists, OuterRef

from foodgram_project.settings import SLUG_MAX_LENGTH

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=30, verbose_name='Наименование тега', unique=True)
    checkbox_style = models.CharField(max_length=30, verbose_name='Цвет чекбокса')

    class Meta:
        verbose_name_plural = 'Теги'
        ordering = ['pk']

    def __str__(self):
        return self.title[0:15]


class Ingredient(models.Model):
    name = models.CharField('Ингредиент', db_index=True, max_length=200, help_text='Название ингредиента')
    dimension = models.CharField('Единица измерения', db_index=True, max_length=200, help_text='Единица измерения')

    class Meta:
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[0:30]


class ReсipeQuerySet(models.QuerySet):

    def get_additional_attributes(self, user, tags=None):
        if user.is_authenticated:
            subquery_favorite = Favorite.objects.filter(recipe=OuterRef('pk'), user=user)
            subquery_shoplist = ShopList.objects.filter(recipe=OuterRef('pk'), user=user)
            if tags:
                return self.filter(
                    tags__in=tags
                ).annotate(
                    favorite_flag=Exists(subquery_favorite),
                    shoplist_flag=Exists(subquery_shoplist)
                )
            return self.annotate(favorite_flag=Exists(subquery_favorite), shoplist_flag=Exists(subquery_shoplist))
        return self.all()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=CASCADE,
        related_name='recipes',
        help_text='Автор'
    )
    title = models.CharField('Название рецепта', db_index=True, max_length=200, help_text='Название')
    image = models.ImageField('Загрузить фото', upload_to='foodgram_images/', help_text='Изображение')
    text = models.TextField('Описание', help_text='Текст рецепта')
    ingredients = models.ManyToManyField(Ingredient, through='QuantityOfIngredient')
    tags = models.ManyToManyField(Tag, verbose_name='Тег', related_name='recipe')
    time = models.IntegerField(
        'Время приготовления',
        validators=[MaxValueValidator(1440)],
        help_text='Время приготовления'
    )
    slug = models.SlugField(
        'Идентификатор рецепта',
        unique=True,
        help_text='Идентификатор рецепта',
        allow_unicode=True,
        max_length=SLUG_MAX_LENGTH
    )
    pub_date = models.DateTimeField('Время публикации', auto_now_add=True, )
    objects = ReсipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title[0:30]


class QuantityOfIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE, verbose_name='Игредиент', help_text='Игредиент')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, verbose_name='Рецепт', help_text='Рецепт')
    quantity = models.IntegerField('Количество', help_text='Количество')

    class Meta:
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        ingredient = self.ingredient.name
        quantity = self.quantity
        output = f'ingredient: {ingredient}, quantity: {quantity}'
        return output[0:30]


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='follower', help_text='Подписчик')
    author = models.ForeignKey(User, on_delete=CASCADE, related_name='following', help_text='Публицист')

    class Meta:
        ordering = ['user', 'author']
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique together'),
            ]
        verbose_name_plural = 'Подписка на авторов'

    def __str__(self):
        user = self.user.username
        author = self.author.username
        output = f'user: {user}, author: {author}'
        return output[0:30]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='favorite_recipe', help_text='Подписчик')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, related_name='favorite_user')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='favorite unique'),
            ]
        verbose_name_plural = 'Список избранного'

    def __str__(self):
        user = self.user.username
        recipe = self.recipe.title
        output = f'user: {user}, recipe: {recipe}'
        return output[0:30]


class ShopList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shop_list',
        verbose_name='Покупатель',
        help_text='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='customer',
        verbose_name='Рецепт',
        help_text='Рецепт'
    )

    class Meta:
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        user = self.user.username
        recipe = self.recipe.title
        output = f'user: {user}, recipe: {recipe}'
        return output[0:30]

from django.contrib import admin

from .models import Favorite, Follow, Ingredient, QuantityOfIngredient, Recipe, ShopList, Tag


class Quantity(admin.TabularInline):
    model = QuantityOfIngredient
    extra = 1


class FoodgramRecipe(admin.ModelAdmin):
    list_display = ['author_short_name', 'title', 'get_ingerdients', 'get_tags', 'pub_date']
    fields = ('author', 'slug', 'title', 'tags', 'time', 'text', 'image')
    search_fields = ('title',)
    list_filter = ('author',)
    autocomplete_fields = ('ingredients',)
    inlines = (Quantity,)
    empty_value_display = '-пусто-'

    def get_tags(self, obj):
        return list(obj.tags.values_list('title', flat=True))

    def author_short_name(self, obj):
        return (obj.author.get_short_name())

    def get_ingerdients(self, obj):
        return list(obj.ingredients.values_list('name', flat=True))

    author_short_name.short_description = 'Автор'
    get_tags.short_description = 'Теги'
    get_ingerdients.short_description = 'Ингредиенты'


class FoodgramTag(admin.ModelAdmin):
    list_display = ['pk', 'title', 'checkbox_style']
    empty_value_display = '-пусто-'


class FoodgramIngridient(admin.ModelAdmin):
    list_display = ['pk', 'name', 'dimension']
    search_fields = ('name',)


class FoodgramQuantityOfIngredient(admin.ModelAdmin):
    list_display = ['pk', 'ingredient', 'recipe', 'quantity']
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author_short_name', 'user_short_name')

    def author_short_name(self, obj):
        return (obj.author.get_short_name())

    def user_short_name(self, obj):
        return (obj.user.get_short_name())

    author_short_name.short_description = 'Автор'
    user_short_name.short_description = 'Подписчик'


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_short_name', 'recipe')

    def user_short_name(self, obj):
        return (obj.user.get_short_name())

    user_short_name.short_description = 'Пользователь'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_short_name', 'recipe')

    def user_short_name(self, obj):
        return (obj.user.get_short_name())

    user_short_name.short_description = 'Пользователь'


admin.site.register(Tag, FoodgramTag)
admin.site.register(Recipe, FoodgramRecipe)
admin.site.register(Ingredient, FoodgramIngridient)
admin.site.register(QuantityOfIngredient, FoodgramQuantityOfIngredient)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShopList, ShopListAdmin)

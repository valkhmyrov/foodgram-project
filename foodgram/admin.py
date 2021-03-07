from django.contrib import admin

from .models import Ingredient, QuantityOfIngredient, Recipe, Tag, Follow, Favorite, ShopList


class FoodgramRecipe(admin.ModelAdmin):
    list_display = ['title', 'author', 'text', 'time', 'pub_date', 'get_tags']
    search_fields = ('title',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'

    def get_tags(self, obj):
        return list(obj.tags.values_list('title', flat=True))

    get_tags.short_description = 'Теги'


class FoodgramTag(admin.ModelAdmin):
    list_display = ['title', 'checkbox_style']
    empty_value_display = '-пусто-'


class FoodgramIngridient(admin.ModelAdmin):
    list_display = ['name', 'dimension']
    search_fields = ('name',)


class FoodgramQuantityOfIngredient(admin.ModelAdmin):
    list_display = ['ingredient', 'recipe', 'quantity']
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_short_name', 'recipe')

    def user_short_name(self, obj):
        return (obj.user.get_short_name())

    user_short_name.short_description = 'Пользователь'

admin.site.register(Tag, FoodgramTag)
admin.site.register(Recipe, FoodgramRecipe)
admin.site.register(Ingredient, FoodgramIngridient)
admin.site.register(QuantityOfIngredient, FoodgramQuantityOfIngredient)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShopList, ShopListAdmin)

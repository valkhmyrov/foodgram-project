from django.contrib import admin

from .models import Ingredient, QuantityOfIngredient, Recipe, Tag


# Завписать теги
class FoodgramRecipe(admin.ModelAdmin):
    list_display = ['title', 'author', 'text', 'time', 'pub_date', ]
    search_fields = ('title',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'

    #def get_tags(self, obj):
    #    return obj.tag__name

class FoodgramTag(admin.ModelAdmin):
    list_display = ['title', 'checkbox_style']
    empty_value_display = '-пусто-'


class FoodgramDimensionOfIngredient(admin.ModelAdmin):
    list_display = ['ingredient', 'dimension', 'recipe', ]
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'

admin.site.register(Tag, FoodgramTag)
admin.site.register(Recipe, FoodgramRecipe)
admin.site.register(Ingredient)
admin.site.register(QuantityOfIngredient)
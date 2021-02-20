from django.contrib import admin

from .models import Recipe


class FoodgramRecipe(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ['author', 'title']


admin.site.register(Recipe, FoodgramRecipe)

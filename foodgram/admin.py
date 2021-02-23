from django.contrib import admin
from django import forms
from .models import Tag, Recipe, Ingredient, QuantityOfIngredient


#class FoodgramTagForm(forms.ModelForm):


# Завписать теги
class FoodgramRecipe(admin.ModelAdmin):
    list_display = ['title', 'author', 'text', 'time']
    search_fields = ('title',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'

    #def get_tags(self, obj):
    #    return obj.tag__name

class FoodgramTag(admin.ModelAdmin):
    list_display = ['tag', ]
    empty_value_display = '-пусто-'


class FoodgramDimensionOfIngredient(admin.ModelAdmin):
    list_display = ['ingredient', 'dimension', 'recipe', ]
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'

admin.site.register(Tag, FoodgramTag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(QuantityOfIngredient)
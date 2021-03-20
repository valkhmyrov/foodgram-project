from django import forms

from .extras import extract_ingredients
from .models import Ingredient, Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', 'ingredients', 'pub_date', 'slug')
        widgets = {'tags': forms.CheckboxSelectMultiple(), 'text': forms.Textarea(attrs={'rows': 8})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredients = extract_ingredients(self.data)

    def clean(self, *args, **kwargs):
        super().clean()
        if not self.ingredients:
            return self.add_error(None, 'Необходимо указать хотя бы один ингредиент для рецепта')
        uniq_ingredients = list({(v['name'], v['dimension']): v for v in self.ingredients}.values())
        if len(uniq_ingredients) != len(self.ingredients):
            return self.add_error(None, 'Исключите дублирование ингредиентов')
        for ingredient in self.ingredients:
            if not Ingredient.objects.filter(name=ingredient['name'], dimension=ingredient['dimension']):
                return self.add_error(None, f"Ингредиента \"{ingredient['name']}\" нет.")

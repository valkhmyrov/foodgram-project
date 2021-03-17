from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', 'ingredients', 'pub_date', 'slug')
        widgets = {'tags': forms.CheckboxSelectMultiple(), 'text': forms.Textarea(attrs={'rows': 8})}

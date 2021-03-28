from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from foodgram_project.settings import SLUG_MAX_LENGTH, SLUG_MAX_TEXT_LENGTH

from .models import Ingredient, QuantityOfIngredient, Recipe, Tag


def setting_all_tags():
    get_parameters = f"?filter={'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    return get_parameters


def extract_ingredients(data):
    output = []
    numbers = [key.replace('nameIngredient_', '') for key, val in data.items() if 'nameIngredient' in key]
    for number in numbers:
        output.append({
            'name': data[f'nameIngredient_{str(number)}'],
            'quantity': int(data[f'valueIngredient_{str(number)}']),
            'dimension': data[f'unitsIngredient_{str(number)}']
        })
    return output


def slug_generate(recipe, form):
    slug_candidate = slug_original = slugify(recipe.title, allow_unicode=True)[:SLUG_MAX_TEXT_LENGTH]
    index = 0
    while Recipe.objects.filter(slug=slug_candidate):
        index += 1
        slug_candidate = f'{slug_original}-{index}'
    if index > int((SLUG_MAX_LENGTH - SLUG_MAX_TEXT_LENGTH) * '9'):
        form.add_error('title', 'С таким заголовком уже много рецептов!')
        return False
    return slug_candidate


def recipe_save(request, form):
    data = []
    recipe = form.save(commit=False)
    recipe.author = request.user
    slug = slug_generate(recipe, form)
    if not slug:
        return False
    recipe.slug = slug
    recipe.save()
    ingredients = extract_ingredients(request.POST)
    for item in ingredients:
        ingredient = get_object_or_404(Ingredient, name=item['name'], dimension=item['dimension'])
        data.append(QuantityOfIngredient(ingredient=ingredient, recipe=recipe, quantity=item['quantity']))
    recipe.ingredients.clear()
    QuantityOfIngredient.objects.bulk_create(data)
    form.save_m2m()
    return True

from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from foodgram_project.settings import SLUG_MAX_LENGTH, SLUG_MAX_TEXT_LENGTH
from .models import Ingredient, QuantityOfIngredient, Tag, Recipe


def getting_tags(request, tag_name):
    tags = Tag.objects.filter(title__in=request.GET.getlist(tag_name))
    return tags


def setting_all_tags():
    get_parameters = '?filter=' + '&filter='.join(Tag.objects.values_list('title', flat=True))
    return get_parameters


def extract_ingredients(data):
    output = []
    numbers = [key.replace('nameIngredient_', '') for key, val in data.items() if 'nameIngredient' in key]
    for number in numbers:
        output.append({
            'name': data['nameIngredient_' + str(number)],
            'quantity': int(data['valueIngredient_' + str(number)]),
            'dimension': data['unitsIngredient_' + str(number)]
        })
    return output


def recipe_save(request, form):
    data = []
    recipe = form.save(commit=False)
    recipe.author = request.user
    slug_candidate = slug_original = slugify(recipe.title, allow_unicode=True)[:SLUG_MAX_TEXT_LENGTH]
    index = 0
    while Recipe.objects.filter(slug=slug_candidate):
        index += 1
        slug_candidate = f'{slug_original}-{index}'
    if index > int((SLUG_MAX_LENGTH - SLUG_MAX_TEXT_LENGTH) * '9'):
        form.add_error('title', 'С таким заголовком уже много рецептов!')
        return False
    recipe.slug = slug_candidate
    recipe.save()
    ingredients = extract_ingredients(request.POST)
    for item in ingredients:
        ingredient = get_object_or_404(Ingredient, name=item['name'], dimension=item['dimension'])
        data.append(QuantityOfIngredient(ingredient=ingredient, recipe=recipe, quantity=item['quantity']))
    QuantityOfIngredient.objects.bulk_create(data)
    form.save_m2m()
    return True

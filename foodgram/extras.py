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


def extract_ingredients(request):
    output = []
    numbers = [key.replace('nameIngredient_', '') for key, val in request.POST.items() if 'nameIngredient' in key]
    for number in numbers:
        output.append({
            'name': request.POST['nameIngredient_' + str(number)],
            'quantity': int(request.POST['valueIngredient_' + str(number)]),
            'dimension': request.POST['unitsIngredient_' + str(number)]
        })
    return output


def ingredients_checkup(request, form):
    if request.method == 'POST':
        ingredients = extract_ingredients(request)
        if not ingredients:
            return form.add_error(None, 'Необходимо указать хотя бы один ингредиент для рецепта')
        uniq_ingredients = list({(v['name'], v['dimension']): v for v in ingredients}.values())
        if len(uniq_ingredients) != len(ingredients):
            return form.add_error(None, 'Исключите дублирование ингредиентов')
        for ingredient in ingredients:
            if not Ingredient.objects.filter(name=ingredient['name'], dimension=ingredient['dimension']):
                return form.add_error(None, 'Ингредиента "' + ingredient['name'] + '" нет.')


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
    ingredients = extract_ingredients(request)
    for item in ingredients:
        ingredient = get_object_or_404(Ingredient, name=item['name'], dimension=item['dimension'])
        data.append(QuantityOfIngredient(ingredient=ingredient, recipe=recipe, quantity=item['quantity']))
    QuantityOfIngredient.objects.bulk_create(data)
    form.save_m2m()
    return True

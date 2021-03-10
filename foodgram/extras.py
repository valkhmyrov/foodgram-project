from django.shortcuts import get_object_or_404

from .models import Tag, QuantityOfIngredient, Ingredient


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
        for ingredient in ingredients:
            if not Ingredient.objects.filter(name=ingredient['name'], dimension=ingredient['dimension']):
                return form.add_error(None, 'Ингредиента "' + ingredient['name'] + '" нет.')

def recipe_save(request, form):
    data = []
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    ingredients = extract_ingredients(request)
    for item in ingredients:
        ingredient = Ingredient.objects.get(name=item['name'], dimension=item['dimension'])
        data.append(QuantityOfIngredient(ingredient=ingredient, recipe=recipe, quantity=item['quantity']))
    QuantityOfIngredient.objects.bulk_create(data)
    form.save_m2m()
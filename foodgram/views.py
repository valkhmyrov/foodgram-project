import json
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, get_object_or_404
from .models import Recipe, Tag, Follow, Ingredient, ShopList, Favorite, QuantityOfIngredient
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.cache import cache_page

from .forms import RecipeForm
from .extras import getting_tags, setting_all_tags, ingredients_checkup, recipe_save


User = get_user_model()


@cache_page(30)
def index(request):
    tags_all = Tag.objects.all()
    tags = getting_tags(request, 'filter')
    if not tags:
        return redirect(reverse('index') + setting_all_tags())
    recipes_list = Recipe.objects.filter(
        tags__in=tags
    ).distinct().select_related(
        'author'
    ).prefetch_related(
        'tags'
    )
    paginator = Paginator(recipes_list, settings.PAGINATOR_ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags_all
    }
    return render(request, 'foodgram/index.html', context)


@cache_page(60)
def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe.objects.prefetch_related('tags'), slug=slug)
    context = {'recipe': recipe}
    return render(request, 'foodgram/recipe.html', context)


@cache_page(60)
def profile(request, username):
    author = get_object_or_404(User, username=username)
    tags_all = Tag.objects.all()
    tags = getting_tags(request, 'filter')
    if not tags:
        return redirect(reverse('profile', args=[author.username]) + setting_all_tags())
    recipes_list = author.recipes.filter(
        tags__in=tags
    ).distinct().select_related(
        'author'
    ).prefetch_related(
        'tags'
    )
    paginator = Paginator(recipes_list, settings.PAGINATOR_ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'tags': tags_all
    }
    return render(request, 'foodgram/profile.html', context)


@login_required
def follow_index(request):
    authors = request.user.follower.all()
    paginator = Paginator(authors, settings.PAGINATOR_FOLLOW_ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'foodgram/follow.html', context)


@login_required
def favorites_index(request):
    tags_all = Tag.objects.all()
    tags = getting_tags(request, 'filter')
    if not tags:
        return redirect(reverse('favorites_index') + setting_all_tags())
    favorites = request.user.favorite_recipe.filter(
        recipe__tags__in=tags
    ).distinct().select_related(
        'recipe'
    )
    paginator = Paginator(favorites, settings.PAGINATOR_FOLLOW_ITEMS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'tags': tags_all}
    return render(request, 'foodgram/favorites.html', context)


@login_required
def shop_list_index(request):
    shop_list = request.user.shop_list.all().prefetch_related('recipe')
    context = {'page': shop_list}
    return render(request, 'foodgram/shop_list.html', context)


@login_required
def shoplist_download(request):
    recipes = request.user.shop_list.values_list('recipe', flat=True)
    if not recipes:
        return redirect(reverse('index'))
    shop_list = QuantityOfIngredient.objects.filter(
        recipe__in = recipes
    ).values(
        'ingredient__name',
        'ingredient__dimension'
    ).annotate(
        Sum('quantity')
    )
    file_data = 'Список ингредиентов\n'
    file_data += '\n'.join(
        [
            f"{i}. {x['ingredient__name']} ({x['ingredient__dimension']}) - {x['quantity__sum']}" 
            for i, x 
            in enumerate(shop_list, start=1)
        ]
    )
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ingredients.txt"'
    return response


@login_required
def purchase_add(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(json_data['id']))
        purchase = ShopList(user=request.user, recipe=recipe)
        purchase.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}) 


# Происходит отправка удаления сразу двумя способами (GET и DELETE) со странички shoplist,
# Тем самым вызывая ошибки. В темплейте shop_list.html закомментировал ShopList.js, в котором реализовано удаление.
# Не доработка фронта, или моя проблема?
@login_required
def purchase_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    purchase = get_object_or_404(ShopList, user=request.user, recipe=recipe)
    purchase.delete()
    if request.method == 'GET':
        if not request.user.shop_list.all():
            return redirect(reverse('index'))
        return redirect(reverse('shop_list_index'))
    if request.method == 'DELETE':
        return JsonResponse({'success': True})


@login_required
def subscription_add(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        author = get_object_or_404(User, id=int(json_data['id']))
        subscription = Follow(author=author, user=request.user)
        subscription.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}) 


@login_required
def subscription_delete(request, id):
    if request.method == 'DELETE':
        author = get_object_or_404(User, id=id)
        subscription = get_object_or_404(Follow, author=author, user=request.user)
        subscription.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}) 


@login_required
def favorite_add(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(json_data['id']))
        favorite = Favorite(user=request.user, recipe=recipe)
        favorite.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}) 


@login_required
def favorite_delete(request, id):
    if request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=id)
        favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe)
        favorite.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}) 


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients_checkup(request, form)
    if form.is_valid():
        recipe_save(request, form)
        return redirect('index')
    return render(request, 'foodgram/new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect('recipe', slug)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    ingredients_checkup(request, form)
    if form.is_valid():
        recipe.ingredients.clear()
        recipe_save(request, form)
        return redirect('recipe', slug)
    context = {'form': form, 'recipe': recipe}
    return render(request, 'foodgram/new_recipe.html', context)


@login_required
def get_ingredients(request):
    ingredient_pattern = request.GET.get('query')
    if ingredient_pattern:
        ingredients = Ingredient.objects.filter(name__icontains=ingredient_pattern).values('name', 'dimension')
        if ingredients:
            data = [{'title': item['name'], 'dimension': item['dimension']} for item in ingredients]
            return JsonResponse(data, safe=False)    
    return JsonResponse([{'title': 'Ингредиент не существует', 'dimension': ''}], safe=False)


@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect('recipe', slug)
    recipe.delete()
    return redirect('profile', request.user)



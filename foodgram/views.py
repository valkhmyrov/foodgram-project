import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .extras import getting_tags, recipe_save, setting_all_tags
from .forms import RecipeForm
from .models import Favorite, Follow, Ingredient, QuantityOfIngredient, Recipe, ShopList, Tag

User = get_user_model()


SUCCESS = JsonResponse({'success': True})
FAILURE = JsonResponse({'success': False}, status=404)


def index(request):
    tags_all = Tag.objects.all()
    tags = getting_tags(request, 'filter')
    if not tags:
        return redirect(f"{reverse('index')}{setting_all_tags()}")
    recipes_list = Recipe.objects.get_additional_attributes(
        request.user,
        tags
    ).distinct().select_related(
        'author'
    )
    paginator = Paginator(recipes_list, settings.PAGINATOR_ITEMS)
    page_number = request.GET.get('page')
    if page_number and int(page_number) not in range(1, paginator.num_pages+1):
        return redirect(f"{reverse('index')}?filter={'&filter='.join(tags.values_list('title', flat=True))}")
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags_all
    }
    return render(request, 'foodgram/index.html', context)


def recipe_view(request, slug):
    recipe = get_object_or_404(
        Recipe.objects.get_additional_attributes(request.user).prefetch_related('tags'), slug=slug
    )
    context = {'recipe': recipe}
    return render(request, 'foodgram/recipe.html', context)


def profile(request, username):
    author = get_object_or_404(User.objects.prefetch_related('follower'), username=username)
    tags_all = Tag.objects.all()
    tags = getting_tags(request, 'filter')
    if not tags:
        return redirect(f"{reverse('profile', args=[author.username])}{setting_all_tags()}")
    recipes_list = Recipe.objects.filter(
        author=author
    ).get_additional_attributes(
        request.user,
        tags
    ).distinct().select_related(
        'author'
    )
    paginator = Paginator(recipes_list, settings.PAGINATOR_ITEMS)
    page_number = request.GET.get('page')
    if page_number and int(page_number) not in range(1, paginator.num_pages+1):
        return redirect(
            f"{reverse('profile', args=[author.username])}?filter="
            f"{'&filter='.join(tags.values_list('title', flat=True))}"
        )
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
    if page_number and int(page_number) not in range(1, paginator.num_pages+1):
        return redirect(reverse('follow_index'))
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'foodgram/follow.html', context)


@login_required
def favorites_index(request):
    tags_all = Tag.objects.all()
    tags = getting_tags(request, 'filter')
    if not tags:
        return redirect(f"{reverse('favorites_index')}{setting_all_tags()}")
    favorites = Recipe.objects.filter(favorite_user__user=request.user).get_additional_attributes(
        request.user,
        tags
    ).distinct().select_related(
        'author'
    )
    paginator = Paginator(favorites, settings.PAGINATOR_ITEMS)
    page_number = request.GET.get('page')
    if page_number and int(page_number) not in range(1, paginator.num_pages+1):
        return redirect(f"{reverse('favorites_index')}?filter={'&filter='.join(tags.values_list('title', flat=True))}")
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
        recipe__in=recipes
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
        return SUCCESS
    return FAILURE


# Происходит отправка удаления сразу двумя способами (GET и DELETE) со странички shoplist, в браузере.
# Тем самым вызывая ошибки. В темплейте shop_list.html закомментировал ShopList.js, в котором реализовано удаление.
@login_required
@require_http_methods(["GET", "DELETE"])
def purchase_delete(request, id):
    purchase = get_object_or_404(ShopList, user=request.user, recipe=id)
    purchase.delete()
    if request.method == 'GET':
        if not request.user.shop_list.all():
            return redirect(reverse('index'))
        return redirect(reverse('shop_list_index'))
    if request.method == 'DELETE':
        return SUCCESS
    else:
        return FAILURE


@login_required
def subscription_add(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        author = get_object_or_404(User, id=int(json_data['id']))
        subscription = Follow(author=author, user=request.user)
        subscription.save()
        return SUCCESS
    return FAILURE


@login_required
def subscription_delete(request, id):
    if request.method == 'DELETE':
        author = get_object_or_404(User, id=id)
        subscription = get_object_or_404(Follow, author=author, user=request.user)
        subscription.delete()
        return SUCCESS
    return FAILURE


@login_required
def favorite_add(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        recipe = get_object_or_404(Recipe, id=int(json_data['id']))
        favorite = Favorite(user=request.user, recipe=recipe)
        favorite.save()
        return SUCCESS
    return FAILURE


@login_required
def favorite_delete(request, id):
    if request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=id)
        favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe)
        favorite.delete()
        return SUCCESS
    return FAILURE


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        if recipe_save(request, form):
            return redirect('index')
    return render(request, 'foodgram/recipe_new.html', {'form': form})


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect('recipe', recipe.slug)

    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if not form.ingredients:
        for ingr in recipe.ingredients.all():
            form.ingredients.append(
                {
                    'name': ingr.name,
                    'quantity': recipe.quantityofingredient_set.filter(ingredient=ingr)[0].quantity,
                    'dimension': ingr.dimension
                }
            )

    if form.is_valid():
        recipe.ingredients.clear()
        recipe_save(request, form)
        return redirect('recipe', recipe.slug)
    context = {'form': form, 'recipe': recipe}
    return render(request, 'foodgram/recipe_new.html', context)


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

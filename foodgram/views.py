from django.shortcuts import redirect, render, get_object_or_404
from .models import Recipe, Tag
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import RecipeForm
from .extras import getting_tags, setting_all_tags


User = get_user_model()


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
    ).order_by(
        '-pub_date'
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


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    context = {'recipe': recipe}
    return render(request, 'foodgram/recipe.html', context)


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
    ).order_by(
        '-pub_date'
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







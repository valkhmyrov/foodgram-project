from django import template
from django.utils.encoding import iri_to_uri

from foodgram.models import Tag

register = template.Library()


@register.filter
def get_list(request, key):
    tags_list = request.GET.getlist(key)
    return tags_list


@register.filter
def filter_manager(request, tag):
    new_request = request.GET.copy()
    if tag.title in request.GET.getlist('filter'):
        filters = new_request.getlist('filter')
        filters.remove(tag.title)
        new_request.setlist('filter', filters)
    else:
        new_request.appendlist('filter', tag.title)
    new_request.pop('page', None)
    return new_request.urlencode()


@register.filter
def paginator_manager(request, number):
    new_request = request.GET.copy()
    new_request['page'] = number
    return new_request.urlencode()


@register.filter
def recipe_count(author):
    count = author.recipes.count() - 3
    if count < 1:
        return False
    return count


@register.filter
def check_shoplist(recipe, user):
    if recipe.customer.filter(user=user):
        return True
    return False


@register.filter()
def tag_colour(tag_title):
    color = Tag.objects.filter(title=tag_title).values_list('checkbox_style', flat=True)[0]
    return color


@register.filter()
def tag_id(tag_title):
    id = Tag.objects.filter(title=tag_title).values_list('id', flat=True)[0]
    return id


@register.filter()
def decode_path(path):
    return iri_to_uri(path)


@register.filter
def check_follower(author, user):
    if user.follower.filter(author=author):
        return True
    return False

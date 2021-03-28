from django import template
from django.utils.encoding import iri_to_uri


register = template.Library()


@register.filter
def paginator_manager(request, number):
    new_request = request.GET.copy()
    new_request['page'] = number
    return new_request.urlencode()


@register.filter()
def decode_path(path):
    return iri_to_uri(path)


@register.filter
def declension(number):
    if number in [11, 12, 13, 14]:
        return 'рецептов'
    if number % 10 == 1:
        return 'рецепт'
    if number % 10 in [2, 3, 4]:
        return 'рецепта'
    return 'рецептов'

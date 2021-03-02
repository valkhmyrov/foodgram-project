from django import template
from ..models import Tag

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
    return new_request.urlencode()


@register.filter
def paginator_manager(request, number):
    new_request = request.GET.copy()
    new_request['page'] = number
    return new_request.urlencode()



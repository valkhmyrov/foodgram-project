from django import template


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


@register.filter
def recipe_count(author):
    count = author.recipes.count() - 3
    if count < 1:
        return False
    return count


@register.filter
def check_user(recipe, user):
    if recipe.favorite_user.filter(user=user):
        return True
    return False
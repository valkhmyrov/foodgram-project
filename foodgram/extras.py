from .models import Tag


def getting_tags(request, tag_name):
    tags = Tag.objects.filter(title__in=request.GET.getlist(tag_name))
    return tags

def setting_all_tags():
    get_parameters = '?filter=' + '&filter='.join(Tag.objects.values_list('title', flat=True))
    return get_parameters
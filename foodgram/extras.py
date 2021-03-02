from .models import Tag


def getting_tags(request, tag_name):
    tags = Tag.objects.filter(title__in=request.GET.getlist(tag_name))
    return tags

def setting_all_tags():
    get_parameters = '?filter=' + '&filter='.join([x.title for x in Tag.objects.all()])
    return get_parameters
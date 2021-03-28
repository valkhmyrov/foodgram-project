from .models import Tag


class FoodgramTags:
    def __init__(self, get_response):
        self.get_response = get_response
        self.tags = [{'object': x} for x in Tag.objects.all()]

    def __call__(self, request):
        existing_filters = request.GET.getlist('filter')
        existing_tags = Tag.objects.filter(title__in=existing_filters)
        for tag in self.tags:
            filters = existing_filters.copy()
            if tag['object'].title in existing_filters and len(existing_filters) > 1:
                tag['active'] = True
                filters.remove(tag['object'].title)
            elif tag['object'].title in existing_filters and len(existing_filters) == 1:
                tag['active'] = True
            else:
                tag['active'] = False
                filters.append(tag['object'].title)
            tag['url'] = f"?filter={'&filter='.join(filters)}"
        request.existing_tags = existing_tags
        request.tags = self.tags
        response = self.get_response(request)
        return response

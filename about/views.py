from django.urls import reverse
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about_something.html'
    TITLE = 'Об авторе'
    TEXT = (
        '<p style="margin-bottom: 0cm; line-height: 100%">Здравствуйте! Меня зовут Хмыров '
        'Валентин. Это моя дипломная работа в <a href="https://praktikum.yandex.ru/">Yandex.Практикум</a></p>'
    )
    extra_context = {'title': TITLE, 'text': TEXT}


class AboutTechView(TemplateView):
    template_name = 'about_something.html'
    TITLE = 'Используемое ПО'
    TEXT = (
        '<ul><li><p style="margin-bottom: 0cm; line-height: 100%"><a href="https://www.djangoproject.com/">'
        'Django 3.1.6</a></p>'
        '<li><p style="margin-bottom: 0cm; line-height: 100%"><a href="https://gunicorn.org/">Gunicorn'
        ' 20.0.4</a></p>'
        '<li><p style="margin-bottom: 0cm; line-height: 100%"><a href="https://www.postgresql.org/">PostgreSQL'
        ' 13.1</a></p></ul>'
    )
    extra_context = {'title': TITLE, 'text': TEXT}

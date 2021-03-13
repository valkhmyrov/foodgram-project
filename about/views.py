from django.views.generic.base import TemplateView
from django.urls import reverse


class AboutSomethingView(TemplateView):
    template_name = 'about_something.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path == reverse('about_author'):
            context['title'] = 'Об авторе'
            context['text'] = (
                '<p style="margin-bottom: 0cm; line-height: 100%">Здравствуйте! Меня зовут Хмыров '
                'Валентин. Это моя дипломная работа в <a href="https://praktikum.yandex.ru/">Yandex.Практикум</a></p>'
            )
        if self.request.path == reverse('about_tech'):
            context['title'] = 'Используемое ПО'
            context['text'] = (
                '<ul><li><p style="margin-bottom: 0cm; line-height: 100%"><a href="https://www.djangoproject.com/">'
                'Django 3.1.6</a></p>'
                '<li><p style="margin-bottom: 0cm; line-height: 100%"><a href="https://gunicorn.org/">Gunicorn'
                ' 20.0.4</a></p>'
                '<li><p style="margin-bottom: 0cm; line-height: 100%"><a href="https://www.postgresql.org/">PostgreSQL'
                ' 13.1</a></p></ul>'
            )
        return context

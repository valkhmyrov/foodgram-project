from django.urls import path

from . import views

urlpatterns = [
    path('author/', views.AboutSomethingView.as_view(), name='about_author'),
    path('tech/', views.AboutSomethingView.as_view(), name='about_tech'),
]

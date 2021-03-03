from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<slug:slug>/', views.recipe_view, name='recipe'),
    path('author/<str:username>/', views.profile, name='profile'),
    path('follow/', views.follow_index, name='follow_index'),
    #path('new/', views.new_recipe, name='new_recipe'),
]

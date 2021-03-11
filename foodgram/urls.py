from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<slug:slug>/', views.recipe_view, name='recipe'),
    path('author/<str:username>/', views.profile, name='profile'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorites_index/', views.favorites_index, name='favorites_index'),
    path('favorites/', views.favorite_add, name='favorite_add'),
    path('favorites/<int:id>', views.favorite_delete, name='favorite_delete'),
    path('shoplist/', views.shop_list_index, name='shop_list_index'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('recipe_new/', views.new_recipe, name='new_recipe'),
    path('recipe_edit/<slug:slug>/', views.recipe_edit, name='recipe_edit'),
    path('recipe_delete/<slug:slug>/', views.recipe_delete, name='recipe_delete'),
    path('ingredients/', views.get_ingredients, name='get_ingredients')
]

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('recipe/(?P<slug>[-\w]+)/', views.recipe_view, name='recipe'),
    path('author/<str:username>/', views.profile, name='profile'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorites_index/', views.favorites_index, name='favorites_index'),
    path('favorites/', views.favorite_add, name='favorite_add'),
    path('favorites/<int:id>', views.favorite_delete, name='favorite_delete'),
    path('shoplist/', views.shop_list_index, name='shop_list_index'),
    path('shoplist_download/', views.shoplist_download, name='shoplist_download'),
    path('purchases/', views.purchase_add, name='purchase_add'),
    path('purchases/<int:id>', views.purchase_delete, name='purchases_delete'),
    path('subscriptions/', views.subscription_add, name='subscription_add'),
    path('subscriptions/<int:id>', views.subscription_delete, name='subscription_delete'),
    path('recipe_new/', views.new_recipe, name='new_recipe'),
    re_path('recipe_edit/(?P<slug>[-\w]+)/', views.recipe_edit, name='recipe_edit'),
    re_path('recipe_delete/(?P<slug>[-\w]+)/', views.recipe_delete, name='recipe_delete'),
    path('ingredients/', views.get_ingredients, name='get_ingredients')
]

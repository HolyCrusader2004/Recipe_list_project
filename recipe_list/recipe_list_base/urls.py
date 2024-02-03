from django.urls import path
from .views import Recipe_list, Recipe_detail,Recipe_create,Recipe_edit,Recipe_delete,Recipe_login,Recipe_signup
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Recipe_login.as_view(), name='recipe_login'),
    path('recipe_logout/', LogoutView.as_view(next_page='recipe_login'), name='recipe_logout'),
    path('recipes/', Recipe_list.as_view(), name='Recipes'),
    path('recipe_signup/', Recipe_signup.as_view(), name='recipe_signup'),
    path('recipe/<int:pk>/', Recipe_detail.as_view(), name='Recipe'),
    path('recipe_create/', Recipe_create.as_view(), name='recipe_create'),
    path('recipe_edit/<int:pk>/', Recipe_edit.as_view(), name='recipe_edit'),
    path('recipe_delete/<int:pk>/', Recipe_delete.as_view(), name='recipe_delete'),
]

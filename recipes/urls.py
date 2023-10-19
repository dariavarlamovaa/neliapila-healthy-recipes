from django.urls import path

from recipes import views

urlpatterns = [
    path('add-a-recipe/', views.add_a_recipe, name='add-recipe')
]
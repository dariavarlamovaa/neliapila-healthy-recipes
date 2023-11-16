from django.urls import path
from recipes import views

urlpatterns = [
    path('add-a-recipe/', views.add_a_recipe, name='add-recipe'),
    path('recipe/<pk>', views.show_specific_recipe, name='specific-recipe'),

    path('pdf-view/<pk>', views.get_pdf, name='pdf'),

    path('delete-recipe/<pk>', views.delete_recipe, name='delete-recipe'),

    path('delete-comment/<pk>', views.delete_comment, name='delete-comment')
]
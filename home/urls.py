from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_recipes, name='recipes'),
    path('found-recipes/', views.search_recipes, name='found-recipes'),
    path('', include('user.urls')),

    path('authors/', views.authors, name='authors'),

    path('about-us/', views.about_us, name='about-us')
]

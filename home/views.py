from django.shortcuts import render

from home.utilis import get_sorted_recipes, get_found_recipes
from recipes.models import Recipe


def get_recipes(request):
    recipes = Recipe.objects.filter(is_approved=True)
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''
    if request.GET.get('sort_by'):
        recipes, sort_query = get_sorted_recipes(request)
    context = {'recipes': recipes, 'favorites': favorite_recipes}
    return render(request, 'home/home.html', context)


def search_recipes(request):
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''

    recipes, search_query = get_found_recipes(request)
    recipes_count = recipes.count()
    context = {'recipes': recipes, 'favorites': favorite_recipes, 'recipes_count': recipes_count,
               'search_query': search_query}
    return render(request, 'recipes/found-recipes.html', context)

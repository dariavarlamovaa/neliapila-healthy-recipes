from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from home.utilis import get_sorted_recipes, get_found_recipes
from recipes.models import Recipe


def paginate_recipes(request, recipes, results=6):
    page = request.GET.get('page')
    paginator = Paginator(recipes, results)

    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        recipes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        recipes = paginator.page(page)

    page = int(page)
    left_index = page - 3 if page > 3 else 1
    right_index = page + 4 if page < paginator.num_pages - 3 else paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return recipes, paginator, custom_range


def sort_recipes(request):
    recipes, sort_query = get_sorted_recipes(request)
    recipes = recipes.order_by('-date_created')
    return recipes, sort_query


def get_recipes(request):
    recipes = Recipe.objects.filter(is_approved=True)

    if request.GET.get('sort_by'):
        recipes, sort_query = sort_recipes(request)
    else:
        recipes = recipes.order_by('-date_created')
        sort_query = ''

    recipes_count = recipes.count()
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''

    recipes, paginator, custom_range = paginate_recipes(request, recipes)

    context = {'recipes': recipes, 'favorites': favorite_recipes,
               'recipes_count': recipes_count, 'paginator': paginator, 'custom_range': custom_range,
               'sort_query': sort_query}
    return render(request, 'home/home.html', context)


def search_recipes(request):
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''
    recipes, search_query = get_found_recipes(request)
    recipes_count = recipes.count()

    recipes, paginator, custom_range = paginate_recipes(request, recipes, results=9)

    context = {'recipes': recipes, 'favorites': favorite_recipes, 'recipes_count': recipes_count,
               'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'recipes/found-recipes.html', context)
